"""
Shipment Tracking Router with AI-powered delay prediction
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from app.database.database import get_db
from app.models.models import Shipment
from app.services.weather_service import assess_weather_impact_on_shipment
from app.services.ai_service import predict_shipment_delay_probability

router = APIRouter(
    prefix="/shipment-tracking",
    tags=["shipment-tracking"],
    responses={404: {"description": "Not found"}},
)


class ShipmentDelayPredictionRequest(BaseModel):
    shipment_id: int


class ShipmentDelayPredictionResponse(BaseModel):
    shipment_id: int
    origin: str
    destination: str
    weather_assessment: Dict[str, Any]
    ai_prediction: Dict[str, Any]
    overall_delay_probability: float
    expected_delay_days: int
    recommendations: List[str]


@router.post("/predict-delay", response_model=ShipmentDelayPredictionResponse)
def predict_shipment_delay(
    request: ShipmentDelayPredictionRequest,
    db: Session = Depends(get_db)
):
    """
    AI-powered shipment delay prediction using weather data and logistics analysis
    
    This demonstrates:
    1. Weather API integration for real-time conditions
    2. AI/LLM analysis of multiple risk factors
    3. Intelligent recommendations for logistics optimization
    """
    
    # Get shipment details
    shipment = db.query(Shipment).filter(Shipment.id == request.shipment_id).first()
    
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    # Prepare shipment data for AI analysis
    # Shipment model doesn't have origin/destination, use supplier address
    origin = shipment.supplier.address if shipment.supplier else "Unknown Origin"
    destination = "Company Warehouse"  # Assuming all shipments go to company warehouse
    
    # Get weather assessment for the route
    weather_assessment = assess_weather_impact_on_shipment(
        origin=origin,
        destination=destination,
        route_type=shipment.shipping_method.lower() if shipment.shipping_method else "sea"
    )
    
    shipment_data = {
        "origin": origin,
        "destination": destination,
        "transport_method": shipment.shipping_method,
        "expected_arrival": shipment.expected_arrival.isoformat() if shipment.expected_arrival else None,
        "tracking_number": shipment.tracking_number
    }
    
    # Use AI to predict delay probability
    ai_prediction = predict_shipment_delay_probability(
        shipment_data=shipment_data,
        weather_data=weather_assessment,
        logistics_data={
            "port_congestion": weather_assessment.get("combined_risk_score", 0) > 50,
            "route_status": "normal"
        }
    )
    
    # Combine weather and AI recommendations
    all_recommendations = weather_assessment.get("recommendations", [])
    if ai_prediction.get("recommended_actions"):
        all_recommendations.extend(ai_prediction["recommended_actions"])
    
    # Calculate overall delay probability (weighted average)
    weather_delay_prob = weather_assessment.get("delay_probability", 0)
    ai_delay_prob = ai_prediction.get("delay_probability", 0)
    
    overall_delay_probability = (weather_delay_prob * 0.6 + ai_delay_prob * 0.4)
    
    # Calculate expected delay days
    expected_delay_days = max(
        weather_assessment.get("expected_delay_days", 0),
        ai_prediction.get("expected_delay_days", 0)
    )
    
    return {
        "shipment_id": shipment.id,
        "origin": origin,
        "destination": destination,
        "weather_assessment": weather_assessment,
        "ai_prediction": ai_prediction,
        "overall_delay_probability": round(overall_delay_probability, 2),
        "expected_delay_days": expected_delay_days,
        "recommendations": all_recommendations[:5]  # Top 5 recommendations
    }


@router.get("/shipments/{shipment_id}/status")
def get_shipment_status_with_ai(
    shipment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get shipment status with AI-enhanced insights
    """
    
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    # Get basic shipment info
    origin = getattr(shipment, 'shipping_origin', 'Unknown Origin')
    destination = getattr(shipment, 'shipping_destination', 'Unknown Destination')
    
    shipment_info = {
        "id": shipment.id,
        "origin": origin,
        "destination": destination,
        "status": shipment.status,
        "shipping_method": shipment.shipping_method,
        "expected_arrival": shipment.expected_arrival.isoformat() if shipment.expected_arrival else None,
        "actual_arrival": shipment.actual_arrival.isoformat() if shipment.actual_arrival else None,
        "tracking_number": shipment.tracking_number
    }
    
    # Add AI-powered delay prediction
    try:
        prediction_request = ShipmentDelayPredictionRequest(shipment_id=shipment_id)
        delay_prediction = predict_shipment_delay(prediction_request, db)
        
        shipment_info["delay_prediction"] = {
            "probability": delay_prediction.overall_delay_probability,
            "expected_delay_days": delay_prediction.expected_delay_days,
            "recommendations": delay_prediction.recommendations
        }
    except Exception as e:
        shipment_info["delay_prediction"] = {
            "error": str(e),
            "probability": None
        }
    
    return shipment_info

