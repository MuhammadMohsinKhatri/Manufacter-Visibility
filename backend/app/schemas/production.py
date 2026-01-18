from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductionLineBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity_per_hour: int
    is_active: bool = True

class ProductionLineCreate(ProductionLineBase):
    pass

class ProductionLineResponse(ProductionLineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductionScheduleBase(BaseModel):
    order_id: int
    production_line_id: int
    scheduled_start: datetime
    scheduled_end: datetime
    status: str = "scheduled"
    notes: Optional[str] = None

class ProductionScheduleCreate(ProductionScheduleBase):
    pass

class ProductionScheduleResponse(ProductionScheduleBase):
    id: int
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductionScheduleUpdate(BaseModel):
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ProductionCapacityCheck(BaseModel):
    start_date: datetime
    end_date: datetime
    product_id: Optional[int] = None

class ProductionCapacityResponse(BaseModel):
    available_capacity: List[dict]
    bottlenecks: List[dict]
    recommended_schedule: Optional[dict] = None