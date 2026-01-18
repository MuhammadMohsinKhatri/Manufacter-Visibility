from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.models import SupplierReliability, RiskLevel

class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    reliability: SupplierReliability = SupplierReliability.MEDIUM

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ShipmentBase(BaseModel):
    supplier_id: int
    expected_arrival: datetime
    status: str = "scheduled"
    tracking_number: Optional[str] = None
    shipping_method: Optional[str] = None
    notes: Optional[str] = None

class ShipmentItemBase(BaseModel):
    component_id: int
    quantity: int

class ShipmentCreate(ShipmentBase):
    items: List[ShipmentItemBase]

class ShipmentItemResponse(ShipmentItemBase):
    id: int
    shipment_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ShipmentResponse(ShipmentBase):
    id: int
    actual_arrival: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    items: List[ShipmentItemResponse]

    class Config:
        from_attributes = True

class ShipmentUpdate(BaseModel):
    expected_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    shipping_method: Optional[str] = None
    notes: Optional[str] = None

class ExternalRiskBase(BaseModel):
    risk_type: str  # weather, logistics, geopolitical, market
    region: str
    description: str
    risk_level: RiskLevel
    start_date: datetime
    end_date: Optional[datetime] = None
    data: Optional[Dict[str, Any]] = None

class ExternalRiskCreate(ExternalRiskBase):
    pass

class ExternalRiskResponse(ExternalRiskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RiskAssessmentRequest(BaseModel):
    region: Optional[str] = None
    component_ids: Optional[List[int]] = None
    supplier_ids: Optional[List[int]] = None
    time_horizon_days: int = 30

class RiskAssessmentResponse(BaseModel):
    risks: List[ExternalRiskResponse]
    affected_components: List[Dict[str, Any]]
    affected_suppliers: List[Dict[str, Any]]
    mitigation_suggestions: List[str]
    overall_risk_score: float