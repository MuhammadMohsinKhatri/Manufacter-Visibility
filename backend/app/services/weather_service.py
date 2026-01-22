"""
Weather Service for Shipment Tracking and Delay Prediction
Integrates with OpenWeatherMap API for real-time weather data
"""
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


def get_weather_for_location(
    location: str,
    days_ahead: int = 7
) -> Dict[str, Any]:
    """
    Get weather forecast for a location
    Can use OpenWeatherMap API or simulate data for demo
    """
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        return _fetch_real_weather(location, api_key, days_ahead)
    else:
        # Simulate weather data for demo
        return _simulate_weather_data(location, days_ahead)


def _fetch_real_weather(location: str, api_key: str, days_ahead: int) -> Dict[str, Any]:
    """Fetch real weather data from OpenWeatherMap API"""
    try:
        # Get coordinates for location
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        geo_response = requests.get(geocoding_url, timeout=5)
        
        if geo_response.status_code != 200:
            return _simulate_weather_data(location, days_ahead)
        
        geo_data = geo_response.json()
        if not geo_data:
            return _simulate_weather_data(location, days_ahead)
        
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        
        # Get weather forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        forecast_response = requests.get(forecast_url, timeout=5)
        
        if forecast_response.status_code != 200:
            return _simulate_weather_data(location, days_ahead)
        
        forecast_data = forecast_response.json()
        
        # Analyze forecast for severe weather
        severe_weather = False
        weather_risks = []
        
        for forecast in forecast_data.get('list', [])[:days_ahead * 8]:  # 8 forecasts per day
            weather = forecast.get('weather', [{}])[0]
            main = forecast.get('main', {})
            wind = forecast.get('wind', {})
            
            # Check for severe conditions
            if weather.get('id', 0) < 700:  # Thunderstorm, rain, snow
                severe_weather = True
                weather_risks.append({
                    "time": forecast.get('dt_txt'),
                    "condition": weather.get('main'),
                    "description": weather.get('description')
                })
            
            if wind.get('speed', 0) > 15:  # High wind speed
                severe_weather = True
                weather_risks.append({
                    "time": forecast.get('dt_txt'),
                    "condition": "High Wind",
                    "wind_speed": wind.get('speed')
                })
        
        return {
            "location": location,
            "data_source": "OpenWeatherMap",
            "severe_weather": severe_weather,
            "weather_risks": weather_risks[:5],  # Top 5 risks
            "overall_condition": "Severe" if severe_weather else "Normal",
            "risk_score": len(weather_risks) * 10 if severe_weather else 0
        }
        
    except Exception as e:
        print(f"Weather API error: {e}")
        return _simulate_weather_data(location, days_ahead)


def _simulate_weather_data(location: str, days_ahead: int) -> Dict[str, Any]:
    """
    Simulate weather data for demo purposes
    In production, this would use real weather API
    """
    
    # Simulate severe weather for certain locations to demonstrate functionality
    high_risk_locations = ["Southeast Asia", "South China Sea", "Gulf of Mexico", "North Atlantic"]
    
    is_high_risk = any(risk_loc.lower() in location.lower() for risk_loc in high_risk_locations)
    
    if is_high_risk:
        return {
            "location": location,
            "data_source": "Simulated",
            "severe_weather": True,
            "weather_risks": [
                {
                    "time": (datetime.now() + timedelta(days=2)).isoformat(),
                    "condition": "Tropical Storm",
                    "description": "Tropical storm with heavy rainfall expected"
                },
                {
                    "time": (datetime.now() + timedelta(days=3)).isoformat(),
                    "condition": "High Wind",
                    "description": "Wind speeds up to 80 km/h expected"
                }
            ],
            "overall_condition": "Severe",
            "risk_score": 75,
            "alert": "Severe weather alert - Consider delaying shipments"
        }
    else:
        return {
            "location": location,
            "data_source": "Simulated",
            "severe_weather": False,
            "weather_risks": [],
            "overall_condition": "Normal",
            "risk_score": 10,
            "alert": None
        }


def assess_weather_impact_on_shipment(
    origin: str,
    destination: str,
    route_type: str = "sea"
) -> Dict[str, Any]:
    """
    Assess weather impact on shipment route
    Checks both origin and destination, plus route
    """
    
    origin_weather = get_weather_for_location(origin)
    destination_weather = get_weather_for_location(destination)
    
    # Combine risks
    total_risk_score = origin_weather.get("risk_score", 0) + destination_weather.get("risk_score", 0)
    
    severe_at_origin = origin_weather.get("severe_weather", False)
    severe_at_destination = destination_weather.get("severe_weather", False)
    
    # Determine delay probability based on multiple factors
    base_delay_prob = 5  # Base risk for any shipment
    
    # Factor 1: Shipping method risk
    route_risk_multiplier = {
        "sea": 1.5,      # Sea shipping has higher delay risk
        "ocean": 1.5,
        "air": 0.5,      # Air shipping is faster and more reliable
        "air freight": 0.5,
        "air cargo": 0.5,
        "truck": 1.0,    # Standard risk
        "road": 1.0,
        "train": 0.8,    # Rail is relatively reliable
        "rail": 0.8
    }
    route_multiplier = route_risk_multiplier.get(route_type.lower(), 1.0)
    
    # Factor 2: Weather risk scores (even if not severe)
    origin_risk = origin_weather.get("risk_score", 0)
    dest_risk = destination_weather.get("risk_score", 0)
    weather_risk_contribution = (origin_risk + dest_risk) * 0.3  # 30% weight
    
    # Factor 3: Severe weather impact
    if severe_at_origin and severe_at_destination:
        severe_weather_risk = 70
        expected_delay_days = 5
    elif severe_at_origin or severe_at_destination:
        severe_weather_risk = 45
        expected_delay_days = 3
    else:
        severe_weather_risk = 0
        expected_delay_days = 0
    
    # Calculate final delay probability
    delay_probability = min(
        (base_delay_prob + weather_risk_contribution + severe_weather_risk) * route_multiplier,
        95  # Cap at 95%
    )
    
    # Adjust expected delay days based on route type
    if expected_delay_days > 0:
        if route_type.lower() in ["air", "air freight", "air cargo"]:
            expected_delay_days = max(1, expected_delay_days - 1)  # Air is faster
        elif route_type.lower() in ["sea", "ocean"]:
            expected_delay_days = expected_delay_days + 1  # Sea can have longer delays
    
    recommendations = []
    if delay_probability > 50:
        recommendations.append("Consider alternative shipping route")
        recommendations.append("Notify customer of potential delay")
        recommendations.append("Increase buffer time in delivery schedule")
    
    if severe_at_origin:
        recommendations.append(f"Severe weather at origin ({origin}) - Monitor port operations")
    
    if severe_at_destination:
        recommendations.append(f"Severe weather at destination ({destination}) - Coordinate with receiving warehouse")
    
    return {
        "origin_weather": origin_weather,
        "destination_weather": destination_weather,
        "combined_risk_score": min(total_risk_score, 100),
        "delay_probability": delay_probability,
        "expected_delay_days": expected_delay_days,
        "severe_weather_detected": severe_at_origin or severe_at_destination,
        "recommendations": recommendations,
        "assessment_time": datetime.now().isoformat()
    }

