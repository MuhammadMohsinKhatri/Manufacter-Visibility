from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.models import ProductionLine, ProductionSchedule, Order, Product

def get_production_line(db: Session, line_id: int) -> Optional[ProductionLine]:
    """Get a production line by ID"""
    return db.query(ProductionLine).filter(ProductionLine.id == line_id).first()

def get_production_lines(db: Session, skip: int = 0, limit: int = 100) -> List[ProductionLine]:
    """Get all production lines with pagination"""
    return db.query(ProductionLine).filter(ProductionLine.is_active == True).offset(skip).limit(limit).all()

def create_production_line(
    db: Session, 
    name: str, 
    description: str, 
    capacity_per_hour: int
) -> ProductionLine:
    """Create a new production line"""
    db_line = ProductionLine(
        name=name,
        description=description,
        capacity_per_hour=capacity_per_hour,
        is_active=True
    )
    db.add(db_line)
    db.commit()
    db.refresh(db_line)
    return db_line

def get_production_schedule(db: Session, schedule_id: int) -> Optional[ProductionSchedule]:
    """Get a production schedule by ID"""
    return db.query(ProductionSchedule).filter(ProductionSchedule.id == schedule_id).first()

def get_production_schedules(
    db: Session, 
    start_date: datetime = None, 
    end_date: datetime = None,
    production_line_id: int = None,
    skip: int = 0, 
    limit: int = 100
) -> List[ProductionSchedule]:
    """Get production schedules with filters"""
    query = db.query(ProductionSchedule)
    
    if start_date:
        query = query.filter(ProductionSchedule.scheduled_end >= start_date)
    
    if end_date:
        query = query.filter(ProductionSchedule.scheduled_start <= end_date)
    
    if production_line_id:
        query = query.filter(ProductionSchedule.production_line_id == production_line_id)
    
    return query.offset(skip).limit(limit).all()

def create_production_schedule(
    db: Session,
    order_id: int,
    production_line_id: int,
    scheduled_start: datetime,
    scheduled_end: datetime,
    status: str = "scheduled",
    notes: str = None
) -> ProductionSchedule:
    """Create a new production schedule"""
    db_schedule = ProductionSchedule(
        order_id=order_id,
        production_line_id=production_line_id,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        status=status,
        notes=notes
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def update_production_schedule(
    db: Session,
    schedule_id: int,
    scheduled_start: datetime = None,
    scheduled_end: datetime = None,
    actual_start: datetime = None,
    actual_end: datetime = None,
    status: str = None,
    notes: str = None
) -> Optional[ProductionSchedule]:
    """Update a production schedule"""
    db_schedule = db.query(ProductionSchedule).filter(ProductionSchedule.id == schedule_id).first()
    if not db_schedule:
        return None
    
    if scheduled_start:
        db_schedule.scheduled_start = scheduled_start
    if scheduled_end:
        db_schedule.scheduled_end = scheduled_end
    if actual_start:
        db_schedule.actual_start = actual_start
    if actual_end:
        db_schedule.actual_end = actual_end
    if status:
        db_schedule.status = status
    if notes:
        db_schedule.notes = notes
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def check_production_capacity(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    production_line_id: int = None
) -> Dict[str, Any]:
    """
    Check production capacity availability between dates
    Returns available capacity in hours and bottleneck information
    """
    # Get all active production lines
    if production_line_id:
        production_lines = db.query(ProductionLine).filter(
            ProductionLine.id == production_line_id,
            ProductionLine.is_active == True
        ).all()
    else:
        production_lines = db.query(ProductionLine).filter(
            ProductionLine.is_active == True
        ).all()
    
    if not production_lines:
        return {
            "available_hours": 0,
            "total_capacity_hours": 0,
            "booked_hours": 0,
            "available_percentage": 0,
            "bottlenecks": [],
            "available_slots": []
        }
    
    # Calculate total capacity in hours
    # Fix timezone-aware datetime comparison
    if start_date.tzinfo is not None and end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=start_date.tzinfo)
    elif start_date.tzinfo is None and end_date.tzinfo is not None:
        start_date = start_date.replace(tzinfo=end_date.tzinfo)
    
    days = (end_date - start_date).days + 1
    hours_per_day = 24  # Assuming 24/7 operation - adjust as needed
    
    total_capacity_hours = sum(line.capacity_per_hour * hours_per_day * days for line in production_lines)
    
    # Get all scheduled production during this period
    schedules = get_production_schedules(db, start_date, end_date, production_line_id)
    
    # Calculate booked hours
    booked_hours = 0
    bottlenecks = []
    
    for schedule in schedules:
        # Calculate overlap with requested period
        # Fix timezone issues
        sched_start = schedule.scheduled_start
        sched_end = schedule.scheduled_end
        
        # Ensure all datetimes have same timezone awareness
        if sched_start.tzinfo is None and start_date.tzinfo is not None:
            sched_start = sched_start.replace(tzinfo=start_date.tzinfo)
        elif sched_start.tzinfo is not None and start_date.tzinfo is None:
            sched_start = sched_start.replace(tzinfo=None)
            
        if sched_end.tzinfo is None and end_date.tzinfo is not None:
            sched_end = sched_end.replace(tzinfo=end_date.tzinfo)
        elif sched_end.tzinfo is not None and end_date.tzinfo is None:
            sched_end = sched_end.replace(tzinfo=None)
        
        schedule_start = max(sched_start, start_date)
        schedule_end = min(sched_end, end_date)
        
        if schedule_end > schedule_start:
            duration_hours = (schedule_end - schedule_start).total_seconds() / 3600
            booked_hours += duration_hours
            
            # Check if this creates a bottleneck (high utilization period)
            production_line = next((line for line in production_lines if line.id == schedule.production_line_id), None)
            if production_line:
                # Calculate utilization for this day
                schedule_day = schedule_start.date()
                day_schedules = [s for s in schedules if s.scheduled_start.date() == schedule_day]
                day_booked_hours = sum((min(s.scheduled_end, datetime.combine(schedule_day, datetime.max.time())) - 
                                      max(s.scheduled_start, datetime.combine(schedule_day, datetime.min.time()))).total_seconds() / 3600
                                     for s in day_schedules)
                
                day_capacity = production_line.capacity_per_hour * hours_per_day
                utilization = (day_booked_hours / day_capacity) * 100 if day_capacity > 0 else 0
                
                if utilization > 80:  # 80% threshold for bottleneck
                    bottlenecks.append({
                        "date": schedule_day.isoformat(),
                        "production_line_id": production_line.id,
                        "production_line_name": production_line.name,
                        "utilization": utilization,
                        "booked_hours": day_booked_hours,
                        "capacity_hours": day_capacity
                    })
    
    # Calculate available capacity
    available_hours = max(0, total_capacity_hours - booked_hours)
    available_percentage = (available_hours / total_capacity_hours) * 100 if total_capacity_hours > 0 else 0
    
    # Find available slots (simplified - in real system would be more complex)
    available_slots = []
    current_date = start_date.date()
    end_day = end_date.date()
    
    while current_date <= end_day:
        for line in production_lines:
            # Get schedules for this line on this day
            day_start = datetime.combine(current_date, datetime.min.time())
            day_end = datetime.combine(current_date, datetime.max.time())
            
            day_schedules = [s for s in schedules 
                            if s.production_line_id == line.id and
                               s.scheduled_end >= day_start and
                               s.scheduled_start <= day_end]
            
            # Sort schedules by start time
            day_schedules.sort(key=lambda s: s.scheduled_start)
            
            # Find gaps between schedules
            last_end_time = day_start
            for schedule in day_schedules:
                if schedule.scheduled_start > last_end_time:
                    # There's a gap
                    gap_hours = (schedule.scheduled_start - last_end_time).total_seconds() / 3600
                    if gap_hours >= 2:  # Only consider gaps of at least 2 hours
                        available_slots.append({
                            "date": current_date.isoformat(),
                            "production_line_id": line.id,
                            "production_line_name": line.name,
                            "start_time": last_end_time.isoformat(),
                            "end_time": schedule.scheduled_start.isoformat(),
                            "duration_hours": gap_hours
                        })
                last_end_time = max(last_end_time, schedule.scheduled_end)
            
            # Check for gap after last schedule until end of day
            if last_end_time < day_end:
                gap_hours = (day_end - last_end_time).total_seconds() / 3600
                if gap_hours >= 2:  # Only consider gaps of at least 2 hours
                    available_slots.append({
                        "date": current_date.isoformat(),
                        "production_line_id": line.id,
                        "production_line_name": line.name,
                        "start_time": last_end_time.isoformat(),
                        "end_time": day_end.isoformat(),
                        "duration_hours": gap_hours
                    })
        
        current_date += timedelta(days=1)
    
    return {
        "available_hours": available_hours,
        "total_capacity_hours": total_capacity_hours,
        "booked_hours": booked_hours,
        "available_percentage": available_percentage,
        "bottlenecks": bottlenecks,
        "available_slots": available_slots
    }

def estimate_production_time(
    db: Session,
    product_id: int,
    quantity: int
) -> Dict[str, Any]:
    """
    Estimate production time needed for a product
    Returns estimated hours needed and earliest possible completion date
    """
    # In a real system, this would use more complex logic based on:
    # - Product complexity
    # - Setup time
    # - Production line efficiency
    # - Historical production data
    # For this demo, we'll use a simplified calculation
    
    # Assume 2 hours per unit as a baseline
    base_hours_per_unit = 2
    
    # Get product to check if it exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {
            "success": False,
            "message": f"Product ID {product_id} not found",
            "estimated_hours": 0,
            "earliest_completion_date": None
        }
    
    # Calculate total hours needed
    total_hours = base_hours_per_unit * quantity
    
    # Find earliest available production slot
    now = datetime.utcnow()
    capacity = check_production_capacity(db, now, now + timedelta(days=30))
    
    if not capacity["available_slots"]:
        # No available slots in next 30 days
        return {
            "success": True,
            "message": "No available production slots in next 30 days",
            "estimated_hours": total_hours,
            "earliest_completion_date": now + timedelta(days=31)  # Default fallback
        }
    
    # Find earliest slot with enough capacity
    suitable_slots = [slot for slot in capacity["available_slots"] if slot["duration_hours"] >= total_hours]
    
    if suitable_slots:
        # Sort by start time
        suitable_slots.sort(key=lambda slot: slot["start_time"])
        earliest_slot = suitable_slots[0]
        completion_date = datetime.fromisoformat(earliest_slot["end_time"])
    else:
        # No single slot is big enough, need to combine slots or extend beyond 30 days
        completion_date = now + timedelta(days=31)  # Default fallback
    
    return {
        "success": True,
        "message": "Production time estimated successfully",
        "estimated_hours": total_hours,
        "earliest_completion_date": completion_date
    }