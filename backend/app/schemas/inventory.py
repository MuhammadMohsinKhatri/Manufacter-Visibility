from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ComponentBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str

class ComponentCreate(ComponentBase):
    pass

class ComponentResponse(ComponentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InventoryItemBase(BaseModel):
    component_id: int
    quantity_available: int
    quantity_allocated: int = 0
    reorder_threshold: int = 10
    location: Optional[str] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    component: ComponentResponse

    class Config:
        from_attributes = True

class InventoryItemUpdate(BaseModel):
    quantity_available: Optional[int] = None
    quantity_allocated: Optional[int] = None
    reorder_threshold: Optional[int] = None
    location: Optional[str] = None

class InventoryAllocationRequest(BaseModel):
    component_id: int
    quantity: int
    order_id: int

class InventoryAllocationResponse(BaseModel):
    success: bool
    message: str
    allocated_quantity: int
    remaining_quantity: int