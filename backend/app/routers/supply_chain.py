from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.schemas.supply_chain import (
    SupplierCreate, SupplierResponse,
    ShipmentCreate, ShipmentResponse, ShipmentUpdate,
    ExternalRiskCreate, ExternalRiskResponse,
    RiskAssessmentRequest, RiskAssessmentResponse
)
from app.services.risk_service import (
    get_external_risks, create_external_risk, update_external_risks,
    assess_supply_chain_risks
)

router = APIRouter(
    prefix="/supply-chain",
    tags=["supply-chain"],
    responses={404: {"description": "Not found"}},
)

# External Risk routes
@router.get("/risks/", response_model=List[ExternalRiskResponse])
def read_risks(
    risk_type: str = None,
    region: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get external risks with filters"""
    return get_external_risks(
        db, 
        risk_type=risk_type,
        region=region,
        start_date=start_date,
        end_date=end_date,
        skip=skip, 
        limit=limit
    )

@router.post("/risks/", response_model=ExternalRiskResponse, status_code=status.HTTP_201_CREATED)
def create_risk(risk: ExternalRiskCreate, db: Session = Depends(get_db)):
    """Create a new external risk"""
    return create_external_risk(
        db,
        risk_type=risk.risk_type,
        region=risk.region,
        description=risk.description,
        risk_level=risk.risk_level,
        start_date=risk.start_date,
        end_date=risk.end_date,
        data=risk.data
    )

@router.post("/update-risks/")
def update_risks(db: Session = Depends(get_db)):
    """Update external risks from all sources"""
    return update_external_risks(db)

@router.post("/assess-risks/", response_model=dict)
def assess_risks(assessment: RiskAssessmentRequest, db: Session = Depends(get_db)):
    """Assess supply chain risks based on external factors"""
    return assess_supply_chain_risks(
        db,
        region=assessment.region,
        component_ids=assessment.component_ids,
        supplier_ids=assessment.supplier_ids,
        time_horizon_days=assessment.time_horizon_days
    )