from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.models import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int
    notes: Optional[str] = None
    estimated_delivery: Optional[datetime] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    order_date: datetime
    status: OrderStatus
    actual_delivery: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    notes: Optional[str] = None

class OrderFeasibilityCheck(BaseModel):
    product_ids: List[int]
    quantities: List[int]
    requested_delivery_date: Optional[datetime] = None

class OrderFeasibilityResponse(BaseModel):
    feasible: bool
    earliest_possible_date: datetime
    inventory_constraints: List[str] = []
    production_constraints: List[str] = []
    risk_factors: List[str] = []
    confidence_score: float = Field(..., ge=0, le=100)