"""
Staff and Resource Management Service
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.models import Staff, TaskAssignment, ProductionSchedule


def get_staff(db: Session, staff_id: int) -> Optional[Staff]:
    """Get a staff member by ID"""
    return db.query(Staff).filter(Staff.id == staff_id).first()


def get_all_staff(
    db: Session, 
    department: str = None,
    is_available: bool = None,
    skip: int = 0,
    limit: int = 100
) -> List[Staff]:
    """Get all staff members with optional filters"""
    query = db.query(Staff)
    
    if department:
        query = query.filter(Staff.department == department)
    
    if is_available is not None:
        query = query.filter(Staff.is_available == is_available)
    
    return query.offset(skip).limit(limit).all()


def create_staff(
    db: Session,
    name: str,
    employee_id: str,
    department: str,
    skill_level: str,
    specialization: str,
    hourly_rate: float = 0.0,
    max_hours_per_day: int = 8,
    is_available: bool = True
) -> Staff:
    """Create a new staff member"""
    db_staff = Staff(
        name=name,
        employee_id=employee_id,
        department=department,
        skill_level=skill_level,
        specialization=specialization,
        hourly_rate=hourly_rate,
        max_hours_per_day=max_hours_per_day,
        is_available=is_available
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


def update_staff(
    db: Session,
    staff_id: int,
    name: str = None,
    department: str = None,
    skill_level: str = None,
    specialization: str = None,
    hourly_rate: float = None,
    max_hours_per_day: int = None,
    is_available: bool = None,
    current_workload_hours: float = None
) -> Optional[Staff]:
    """Update a staff member"""
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not db_staff:
        return None
    
    if name is not None:
        db_staff.name = name
    if department is not None:
        db_staff.department = department
    if skill_level is not None:
        db_staff.skill_level = skill_level
    if specialization is not None:
        db_staff.specialization = specialization
    if hourly_rate is not None:
        db_staff.hourly_rate = hourly_rate
    if max_hours_per_day is not None:
        db_staff.max_hours_per_day = max_hours_per_day
    if is_available is not None:
        db_staff.is_available = is_available
    if current_workload_hours is not None:
        db_staff.current_workload_hours = current_workload_hours
    
    db.commit()
    db.refresh(db_staff)
    return db_staff


def get_staff_workload(db: Session, staff_id: int) -> Dict[str, Any]:
    """Get current workload for a staff member"""
    staff = get_staff(db, staff_id)
    if not staff:
        return {"error": "Staff not found"}
    
    # Get active task assignments
    active_tasks = db.query(TaskAssignment).filter(
        TaskAssignment.staff_id == staff_id,
        TaskAssignment.status.in_(["assigned", "in_progress"])
    ).all()
    
    total_assigned_hours = sum(task.assigned_hours for task in active_tasks)
    
    # Get upcoming tasks
    upcoming_tasks = db.query(TaskAssignment).filter(
        TaskAssignment.staff_id == staff_id,
        TaskAssignment.status == "assigned",
        TaskAssignment.start_time >= datetime.utcnow()
    ).order_by(TaskAssignment.start_time).limit(10).all()
    
    return {
        "staff_id": staff_id,
        "staff_name": staff.name,
        "current_workload_hours": staff.current_workload_hours,
        "max_hours_per_day": staff.max_hours_per_day,
        "utilization_percentage": (staff.current_workload_hours / (staff.max_hours_per_day * 7)) * 100 if staff.max_hours_per_day > 0 else 0,
        "active_tasks": len(active_tasks),
        "total_assigned_hours": total_assigned_hours,
        "upcoming_tasks": [
            {
                "task_id": task.id,
                "task_type": task.task_type,
                "start_time": task.start_time.isoformat() if task.start_time else None,
                "end_time": task.end_time.isoformat() if task.end_time else None,
                "assigned_hours": task.assigned_hours
            }
            for task in upcoming_tasks
        ]
    }


def get_task_assignments(
    db: Session,
    production_schedule_id: int = None,
    staff_id: int = None,
    status: str = None
) -> List[TaskAssignment]:
    """Get task assignments with optional filters"""
    query = db.query(TaskAssignment)
    
    if production_schedule_id:
        query = query.filter(TaskAssignment.production_schedule_id == production_schedule_id)
    
    if staff_id:
        query = query.filter(TaskAssignment.staff_id == staff_id)
    
    if status:
        query = query.filter(TaskAssignment.status == status)
    
    return query.all()


def create_task_assignment(
    db: Session,
    production_schedule_id: int,
    staff_id: int,
    task_type: str,
    assigned_hours: float,
    start_time: datetime = None,
    end_time: datetime = None,
    status: str = "assigned",
    notes: str = None
) -> TaskAssignment:
    """Create a new task assignment"""
    db_assignment = TaskAssignment(
        production_schedule_id=production_schedule_id,
        staff_id=staff_id,
        task_type=task_type,
        assigned_hours=assigned_hours,
        start_time=start_time,
        end_time=end_time,
        status=status,
        notes=notes
    )
    db.add(db_assignment)
    
    # Update staff workload
    staff = get_staff(db, staff_id)
    if staff:
        staff.current_workload_hours += assigned_hours
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

