"""
Optimization Router for Production Scheduling and Resource Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.optimization import (
    ProductionOptimizationRequest,
    StaffAssignmentRequest,
    OrderFulfillmentOptimizationRequest,
    StaffCreate,
    StaffUpdate,
    StaffResponse,
    TaskAssignmentResponse
)
from app.services.optimization_service import (
    optimize_production_schedule,
    assign_tasks_to_staff,
    optimize_order_fulfillment
)
from app.services.staff_service import (
    get_staff, get_all_staff, create_staff, update_staff,
    get_staff_workload, get_task_assignments, create_task_assignment
)

router = APIRouter(
    prefix="/optimization",
    tags=["optimization"],
    responses={404: {"description": "Not found"}},
)


@router.post("/production-schedule", response_model=dict)
def optimize_schedule(
    request: ProductionOptimizationRequest,
    db: Session = Depends(get_db)
):
    """
    Optimize production schedule for multiple orders using constraint programming
    """
    result = optimize_production_schedule(
        db,
        request.order_ids,
        request.start_date,
        request.end_date,
        request.objectives
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Optimization failed")
        )
    
    return result


@router.post("/staff-assignment", response_model=dict)
def optimize_staff_assignment(
    request: StaffAssignmentRequest,
    db: Session = Depends(get_db)
):
    """
    Optimize staff assignment for production tasks
    """
    result = assign_tasks_to_staff(
        db,
        request.production_schedule_id,
        [task.dict() for task in request.task_requirements]
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Staff assignment optimization failed")
        )
    
    return result


@router.post("/order-fulfillment", response_model=dict)
def optimize_fulfillment(
    request: OrderFulfillmentOptimizationRequest,
    db: Session = Depends(get_db)
):
    """
    Complete optimization of order fulfillment including:
    - Production scheduling
    - Resource allocation
    - Staff assignment
    """
    result = optimize_order_fulfillment(
        db,
        request.order_ids,
        request.optimize_for,
        request.start_date,
        request.end_date
    )
    
    if not result.get("success"):
        error_detail = result.get("error", "Order fulfillment optimization failed")
        diagnostics = result.get("diagnostics", {})
        
        # Include diagnostics in error message if available
        if diagnostics:
            error_detail += f" Diagnostics: {diagnostics}"
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail
        )
    
    return result


# Staff Management Endpoints
@router.post("/staff", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff_member(
    staff: StaffCreate,
    db: Session = Depends(get_db)
):
    """Create a new staff member"""
    return create_staff(
        db,
        staff.name,
        staff.employee_id,
        staff.department,
        staff.skill_level,
        staff.specialization,
        staff.hourly_rate,
        staff.max_hours_per_day,
        staff.is_available
    )


@router.get("/staff", response_model=List[StaffResponse])
def list_staff(
    department: str = None,
    is_available: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all staff members"""
    return get_all_staff(db, department, is_available, skip, limit)


@router.get("/staff/{staff_id}", response_model=StaffResponse)
def get_staff_member(staff_id: int, db: Session = Depends(get_db)):
    """Get a staff member by ID"""
    staff = get_staff(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff


@router.put("/staff/{staff_id}", response_model=StaffResponse)
def update_staff_member(
    staff_id: int,
    staff_update: StaffUpdate,
    db: Session = Depends(get_db)
):
    """Update a staff member"""
    staff = update_staff(
        db,
        staff_id,
        staff_update.name,
        staff_update.department,
        staff_update.skill_level,
        staff_update.specialization,
        staff_update.hourly_rate,
        staff_update.max_hours_per_day,
        staff_update.is_available,
        staff_update.current_workload_hours
    )
    
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff


@router.get("/staff/{staff_id}/workload", response_model=dict)
def get_staff_workload_info(staff_id: int, db: Session = Depends(get_db)):
    """Get workload information for a staff member"""
    return get_staff_workload(db, staff_id)


@router.get("/task-assignments", response_model=List[TaskAssignmentResponse])
def list_task_assignments(
    production_schedule_id: int = None,
    staff_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get task assignments with optional filters"""
    return get_task_assignments(db, production_schedule_id, staff_id, status)

