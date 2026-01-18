from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import requests
import os
from dotenv import load_dotenv

from app.models.models import ExternalRisk, Component, Supplier, SupplierComponent, Shipment, RiskLevel

load_dotenv()

def get_external_risks(
    db: Session, 
    risk_type: str = None,
    region: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0, 
    limit: int = 100
) -> List[ExternalRisk]:
    """Get external risks with filters"""
    query = db.query(ExternalRisk)
    
    if risk_type:
        query = query.filter(ExternalRisk.risk_type == risk_type)
    
    if region:
        query = query.filter(ExternalRisk.region == region)
    
    if start_date:
        query = query.filter(
            (ExternalRisk.end_date >= start_date) | (ExternalRisk.end_date == None)
        )
    
    if end_date:
        query = query.filter(ExternalRisk.start_date <= end_date)
    
    return query.offset(skip).limit(limit).all()

def create_external_risk(
    db: Session,
    risk_type: str,
    region: str,
    description: str,
    risk_level: RiskLevel,
    start_date: datetime,
    end_date: datetime = None,
    data: Dict[str, Any] = None
) -> ExternalRisk:
    """Create a new external risk"""
    db_risk = ExternalRisk(
        risk_type=risk_type,
        region=region,
        description=description,
        risk_level=risk_level,
        start_date=start_date,
        end_date=end_date,
        data=data
    )
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk

def fetch_weather_risks(region: str = None) -> List[Dict[str, Any]]:
    """
    Fetch weather risks from external API
    In a real system, this would connect to a weather API
    For this demo, we'll return simulated data
    """
    # Simulated weather risks
    return [
        {
            "risk_type": "weather",
            "region": "Southeast Asia",
            "description": "Tropical storm approaching manufacturing hubs",
            "risk_level": RiskLevel.HIGH,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=5),
            "data": {
                "storm_name": "Typhoon Megi",
                "wind_speed": 120,
                "rainfall_mm": 300,
                "affected_areas": ["Vietnam", "Thailand", "Malaysia"]
            }
        },
        {
            "risk_type": "weather",
            "region": "North America",
            "description": "Severe winter storm affecting transportation",
            "risk_level": RiskLevel.MEDIUM,
            "start_date": datetime.utcnow() + timedelta(days=2),
            "end_date": datetime.utcnow() + timedelta(days=4),
            "data": {
                "snowfall_cm": 30,
                "temperature_c": -15,
                "affected_areas": ["Midwest US", "Eastern Canada"]
            }
        }
    ]

def fetch_logistics_risks() -> List[Dict[str, Any]]:
    """
    Fetch logistics risks from external API
    In a real system, this would connect to a logistics/port API
    For this demo, we'll return simulated data
    """
    # Simulated logistics risks
    return [
        {
            "risk_type": "logistics",
            "region": "Asia Pacific",
            "description": "Port congestion at Shanghai port",
            "risk_level": RiskLevel.MEDIUM,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=10),
            "data": {
                "port_name": "Shanghai",
                "congestion_level": "High",
                "average_delay_days": 7,
                "vessels_waiting": 38
            }
        },
        {
            "risk_type": "logistics",
            "region": "Europe",
            "description": "Trucker strike affecting road transport",
            "risk_level": RiskLevel.HIGH,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=14),
            "data": {
                "countries_affected": ["France", "Germany", "Belgium"],
                "estimated_impact": "Severe",
                "alternative_routes": "Limited"
            }
        }
    ]

def fetch_market_risks() -> List[Dict[str, Any]]:
    """
    Fetch market risks related to commodity prices
    In a real system, this would connect to a market data API
    For this demo, we'll return simulated data
    """
    # Simulated market risks
    return [
        {
            "risk_type": "market",
            "region": "Global",
            "description": "Semiconductor shortage affecting electronics supply",
            "risk_level": RiskLevel.CRITICAL,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=90),
            "data": {
                "commodity": "Semiconductors",
                "price_increase_percent": 35,
                "estimated_shortage_months": 6
            }
        },
        {
            "risk_type": "market",
            "region": "Global",
            "description": "Rising steel prices",
            "risk_level": RiskLevel.MEDIUM,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=60),
            "data": {
                "commodity": "Steel",
                "price_increase_percent": 15,
                "main_cause": "Production constraints"
            }
        }
    ]

def fetch_geopolitical_risks() -> List[Dict[str, Any]]:
    """
    Fetch geopolitical risks
    In a real system, this would connect to a risk intelligence API
    For this demo, we'll return simulated data
    """
    # Simulated geopolitical risks
    return [
        {
            "risk_type": "geopolitical",
            "region": "Eastern Europe",
            "description": "Trade restrictions affecting material exports",
            "risk_level": RiskLevel.HIGH,
            "start_date": datetime.utcnow(),
            "end_date": None,  # Indefinite
            "data": {
                "countries_affected": ["Multiple Eastern European countries"],
                "materials_affected": ["Metals", "Energy"],
                "policy_type": "Export controls"
            }
        }
    ]

def update_external_risks(db: Session) -> Dict[str, Any]:
    """
    Update external risks from all sources
    Returns summary of risks added
    """
    # Fetch risks from all sources
    weather_risks = fetch_weather_risks()
    logistics_risks = fetch_logistics_risks()
    market_risks = fetch_market_risks()
    geopolitical_risks = fetch_geopolitical_risks()
    
    all_risks = weather_risks + logistics_risks + market_risks + geopolitical_risks
    
    # Add risks to database
    added_risks = []
    for risk in all_risks:
        # Check if similar risk already exists
        existing_risk = db.query(ExternalRisk).filter(
            ExternalRisk.risk_type == risk["risk_type"],
            ExternalRisk.region == risk["region"],
            ExternalRisk.start_date <= datetime.utcnow(),
            (ExternalRisk.end_date >= datetime.utcnow()) | (ExternalRisk.end_date == None)
        ).first()
        
        if not existing_risk:
            # Add new risk
            db_risk = create_external_risk(
                db,
                risk_type=risk["risk_type"],
                region=risk["region"],
                description=risk["description"],
                risk_level=risk["risk_level"],
                start_date=risk["start_date"],
                end_date=risk["end_date"],
                data=risk["data"]
            )
            added_risks.append(db_risk)
    
    return {
        "success": True,
        "message": f"Added {len(added_risks)} new risks",
        "added_risks": added_risks
    }

def assess_supply_chain_risks(
    db: Session,
    region: str = None,
    component_ids: List[int] = None,
    supplier_ids: List[int] = None,
    time_horizon_days: int = 30
) -> Dict[str, Any]:
    """
    Assess supply chain risks based on external factors
    Returns risk assessment including affected components and suppliers
    """
    # Get relevant external risks
    end_date = datetime.utcnow() + timedelta(days=time_horizon_days)
    risks = get_external_risks(
        db, 
        region=region,
        start_date=datetime.utcnow(),
        end_date=end_date
    )
    
    # Get components and their suppliers
    query = db.query(Component, Supplier)
    
    if component_ids:
        # Filter by specific components
        query = query.join(
            SupplierComponent, SupplierComponent.component_id == Component.id
        ).join(
            Supplier, Supplier.id == SupplierComponent.supplier_id
        ).filter(
            Component.id.in_(component_ids)
        )
    elif supplier_ids:
        # Filter by specific suppliers
        query = query.join(
            SupplierComponent, SupplierComponent.supplier_id == Supplier.id
        ).join(
            Component, Component.id == SupplierComponent.component_id
        ).filter(
            Supplier.id.in_(supplier_ids)
        )
    else:
        # Get all components and suppliers
        query = query.join(
            SupplierComponent, SupplierComponent.component_id == Component.id
        ).join(
            Supplier, Supplier.id == SupplierComponent.supplier_id
        )
    
    component_suppliers = query.all()
    
    # Analyze which components and suppliers are affected by risks
    affected_components = []
    affected_suppliers = []
    
    for component, supplier in component_suppliers:
        # Check if supplier's region is affected by any risks
        supplier_risks = [
            risk for risk in risks 
            if risk.region == supplier.address  # Simplified check - in real system would use geocoding
        ]
        
        if supplier_risks:
            # Component is affected by risks
            if component.id not in [c["component_id"] for c in affected_components]:
                affected_components.append({
                    "component_id": component.id,
                    "component_name": component.name,
                    "risks": [
                        {
                            "risk_id": risk.id,
                            "risk_type": risk.risk_type,
                            "description": risk.description,
                            "risk_level": risk.risk_level.value
                        }
                        for risk in supplier_risks
                    ]
                })
            
            # Supplier is affected by risks
            if supplier.id not in [s["supplier_id"] for s in affected_suppliers]:
                affected_suppliers.append({
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "reliability": supplier.reliability.value,
                    "risks": [
                        {
                            "risk_id": risk.id,
                            "risk_type": risk.risk_type,
                            "description": risk.description,
                            "risk_level": risk.risk_level.value
                        }
                        for risk in supplier_risks
                    ]
                })
    
    # Generate mitigation suggestions
    mitigation_suggestions = []
    
    if affected_components:
        mitigation_suggestions.append(
            f"Consider alternative suppliers for {len(affected_components)} affected components"
        )
    
    if affected_suppliers:
        mitigation_suggestions.append(
            f"Increase safety stock for components from {len(affected_suppliers)} affected suppliers"
        )
    
    high_risks = [risk for risk in risks if risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
    if high_risks:
        mitigation_suggestions.append(
            "Develop contingency plans for high-risk scenarios"
        )
    
    # Calculate overall risk score (0-100)
    risk_score_factors = []
    
    # Factor 1: Number of affected components
    component_factor = min(100, len(affected_components) * 10)
    risk_score_factors.append(component_factor)
    
    # Factor 2: Severity of risks
    severity_mapping = {
        RiskLevel.LOW: 25,
        RiskLevel.MEDIUM: 50,
        RiskLevel.HIGH: 75,
        RiskLevel.CRITICAL: 100
    }
    
    if risks:
        avg_severity = sum(severity_mapping[risk.risk_level] for risk in risks) / len(risks)
    else:
        avg_severity = 0
    
    risk_score_factors.append(avg_severity)
    
    # Factor 3: Supplier reliability (inverse)
    reliability_mapping = {
        "low": 80,
        "medium": 50,
        "high": 20
    }
    
    if affected_suppliers:
        avg_reliability_score = sum(
            reliability_mapping[supplier["reliability"]] 
            for supplier in affected_suppliers
        ) / len(affected_suppliers)
    else:
        avg_reliability_score = 0
    
    risk_score_factors.append(avg_reliability_score)
    
    # Calculate final score - weighted average
    overall_risk_score = (
        component_factor * 0.3 +
        avg_severity * 0.4 +
        avg_reliability_score * 0.3
    )
    
    return {
        "risks": risks,
        "affected_components": affected_components,
        "affected_suppliers": affected_suppliers,
        "mitigation_suggestions": mitigation_suggestions,
        "overall_risk_score": overall_risk_score
    }