from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.schemas.production import (
    ProductionLineCreate, ProductionLineResponse,
    ProductionScheduleCreate, ProductionScheduleResponse, ProductionScheduleUpdate,
    ProductionCapacityCheck, ProductionCapacityResponse
)
from app.services.production_service import (
    get_production_line, get_production_lines, create_production_line,
    get_production_schedule, get_production_schedules, create_production_schedule,
    update_production_schedule, check_production_capacity, estimate_production_time
)

router = APIRouter(
    prefix="/production",
    tags=["production"],
    responses={404: {"description": "Not found"}},
)

# Production Line routes
@router.post("/lines/", response_model=ProductionLineResponse, status_code=status.HTTP_201_CREATED)
def create_new_production_line(line: ProductionLineCreate, db: Session = Depends(get_db)):
    """Create a new production line"""
    return create_production_line(
        db, 
        line.name, 
        line.description, 
        line.capacity_per_hour
    )

@router.get("/lines/", response_model=List[ProductionLineResponse])
def read_production_lines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all production lines"""
    return get_production_lines(db, skip=skip, limit=limit)

@router.get("/lines/{line_id}", response_model=ProductionLineResponse)
def read_production_line(line_id: int, db: Session = Depends(get_db)):
    """Get a production line by ID"""
    db_line = get_production_line(db, line_id=line_id)
    if db_line is None:
        raise HTTPException(status_code=404, detail="Production line not found")
    return db_line

# Production Schedule routes
@router.post("/schedules/", response_model=ProductionScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_new_schedule(schedule: ProductionScheduleCreate, db: Session = Depends(get_db)):
    """Create a new production schedule"""
    # Check if production line exists
    line = get_production_line(db, line_id=schedule.production_line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Production line not found")
    
    return create_production_schedule(
        db,
        schedule.order_id,
        schedule.production_line_id,
        schedule.scheduled_start,
        schedule.scheduled_end,
        schedule.status,
        schedule.notes
    )

@router.get("/schedules/", response_model=List[ProductionScheduleResponse])
def read_schedules(
    start_date: datetime = None, 
    end_date: datetime = None,
    production_line_id: int = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get production schedules with filters"""
    return get_production_schedules(
        db, 
        start_date=start_date, 
        end_date=end_date,
        production_line_id=production_line_id,
        skip=skip, 
        limit=limit
    )

@router.get("/schedules/{schedule_id}", response_model=ProductionScheduleResponse)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Get a production schedule by ID"""
    db_schedule = get_production_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Production schedule not found")
    return db_schedule

@router.put("/schedules/{schedule_id}", response_model=ProductionScheduleResponse)
def update_schedule(schedule_id: int, schedule: ProductionScheduleUpdate, db: Session = Depends(get_db)):
    """Update a production schedule"""
    db_schedule = update_production_schedule(
        db,
        schedule_id=schedule_id,
        scheduled_start=schedule.scheduled_start,
        scheduled_end=schedule.scheduled_end,
        actual_start=schedule.actual_start,
        actual_end=schedule.actual_end,
        status=schedule.status,
        notes=schedule.notes
    )
    
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Production schedule not found")
    
    return db_schedule

@router.post("/check-capacity", response_model=dict)
def check_capacity(capacity_check: ProductionCapacityCheck, db: Session = Depends(get_db)):
    """Check production capacity availability between dates"""
    return check_production_capacity(
        db,
        start_date=capacity_check.start_date,
        end_date=capacity_check.end_date
    )

@router.get("/estimate-time/{product_id}")
def estimate_time(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """Estimate production time needed for a product"""
    result = estimate_production_time(db, product_id, quantity)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result