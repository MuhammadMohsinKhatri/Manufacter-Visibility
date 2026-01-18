"""
AI Service for Manufacturing Visibility System
Uses OpenAI GPT for intelligent decision-making and recommendations
"""
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from datetime import datetime
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend/.env file
# Get the directory where this file is located, then go up to backend/
backend_dir = Path(__file__).parent.parent.parent
env_file = backend_dir / ".env"
load_dotenv(env_file)

# Initialize OpenAI client
client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        api_key_clean = api_key.strip()
        
        # Clear any proxy-related environment variables that might interfere
        # OpenAI client might try to read these automatically and fail
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
        original_proxies = {}
        for var in proxy_vars:
            if var in os.environ:
                original_proxies[var] = os.environ[var]
                del os.environ[var]
        
        try:
            # Initialize OpenAI client with only the api_key parameter
            # Explicitly avoid any proxy configuration
            import inspect
            sig = inspect.signature(OpenAI.__init__)
            params = list(sig.parameters.keys())
            print(f"[DEBUG] AI Service: OpenAI.__init__ parameters: {params}")
            
            # Try to create OpenAI client
            # The error is caused by OpenAI's internal httpx wrapper trying to pass 'proxies' 
            # to httpx.Client() when httpx version doesn't support it
            # Solution: Install compatible httpx version or provide custom http_client
            try:
                import httpx
                # Create httpx client explicitly without proxies
                http_client = httpx.Client()
                print(f"[DEBUG] AI Service: Created httpx client without proxies")
                client_kwargs = {
                    "api_key": api_key_clean,
                    "http_client": http_client
                }
            except ImportError:
                print(f"[DEBUG] AI Service: httpx not found, OpenAI will create its own")
                client_kwargs = {"api_key": api_key_clean}
            
            client = OpenAI(**client_kwargs)
            
            # Verify client was created successfully
            if client is None:
                print("Warning: OpenAI client is None after initialization")
            else:
                print(f"[DEBUG] AI Service: OpenAI client created successfully")
        finally:
            # Restore original proxy environment variables if they existed
            for var, value in original_proxies.items():
                os.environ[var] = value
    else:
        print("Warning: OPENAI_API_KEY not found or empty in environment")
except TypeError as e:
    # Handle OpenAI version compatibility issue
    print(f"[DEBUG] AI Service: TypeError during initialization: {e}")
    try:
        from openai import OpenAI as OpenAIClient
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.strip():
            client = OpenAIClient(api_key=api_key.strip())
            print(f"[DEBUG] AI Service: OpenAI client created via fallback method")
    except Exception as e2:
        print(f"[DEBUG] AI Service: Fallback initialization also failed: {type(e2).__name__}: {e2}")
        import traceback
        print(f"[DEBUG] AI Service: Traceback:\n{traceback.format_exc()}")
except Exception as e:
    print(f"[DEBUG] AI Service: Exception during initialization: {type(e).__name__}: {e}")
    import traceback
    print(f"[DEBUG] AI Service: Full traceback:\n{traceback.format_exc()}")


# Debug: Print client initialization status
print(f"[DEBUG] AI Service: OpenAI client initialized: {client is not None}")
api_key_from_env = os.getenv("OPENAI_API_KEY")
print(f"[DEBUG] AI Service: API key in environment: {api_key_from_env is not None}")
print(f"[DEBUG] AI Service: API key length: {len(api_key_from_env) if api_key_from_env else 0}")
if api_key_from_env:
    print(f"[DEBUG] AI Service: API key starts with 'sk-': {api_key_from_env.startswith('sk-')}")
    print(f"[DEBUG] AI Service: API key first 10 chars: {api_key_from_env[:10]}...")
    print(f"[DEBUG] AI Service: API key last 4 chars: ...{api_key_from_env[-4:]}")
print(f"[DEBUG] AI Service: .env file path: {env_file}")
print(f"[DEBUG] AI Service: .env file exists: {env_file.exists()}")

def analyze_order_feasibility_with_ai(
    order_data: Dict[str, Any],
    inventory_analysis: Dict[str, Any],
    production_analysis: Dict[str, Any],
    risk_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Use AI to analyze order feasibility and provide intelligent recommendations
    
    This goes beyond simple calculations to provide contextual insights
    """
    
    print(f"[DEBUG] analyze_order_feasibility_with_ai: Called")
    print(f"[DEBUG] analyze_order_feasibility_with_ai: Client is None: {client is None}")
    print(f"[DEBUG] analyze_order_feasibility_with_ai: Client type: {type(client)}")
    
    if not client:
        print(f"[DEBUG] analyze_order_feasibility_with_ai: Client is None, using fallback")
        return _fallback_analysis(order_data, inventory_analysis, production_analysis, risk_analysis)
    
    try:
        # Prepare comprehensive context for AI analysis
        context = f"""
You are an AI manufacturing operations consultant analyzing order feasibility.

ORDER DETAILS:
- Products requested: {order_data.get('product_ids', [])}
- Quantities: {order_data.get('quantities', [])}
- Requested delivery date: {order_data.get('requested_delivery_date', 'Not specified')}

INVENTORY ANALYSIS:
- Constraints: {inventory_analysis.get('inventory_constraints', [])}
- Available components: {len([c for c in inventory_analysis.get('inventory_constraints', []) if 'Insufficient' not in c])}

PRODUCTION ANALYSIS:
- Constraints: {production_analysis.get('production_constraints', [])}
- Available capacity: {production_analysis.get('available_hours', 'Unknown')} hours

SUPPLY CHAIN RISKS:
- Risk score: {risk_analysis.get('overall_risk_score', 0)}/100
- Active risks: {len(risk_analysis.get('risks', []))}
- Affected components: {len(risk_analysis.get('affected_components', []))}

Based on this data, provide:
1. A clear GO/NO-GO recommendation
2. The most critical bottleneck
3. Three specific, actionable recommendations to improve feasibility
4. Estimated confidence level (0-100)
5. Alternative strategies if this order cannot be fulfilled as requested

Format your response as JSON with these keys:
- recommendation: "GO" or "NO-GO"
- confidence: number (0-100)
- critical_bottleneck: string
- actionable_recommendations: array of strings (3 items)
- alternative_strategies: array of strings
- executive_summary: string (2-3 sentences for CEO)
"""

        print(f"[DEBUG] analyze_order_feasibility_with_ai: Making API call to OpenAI...")
        print(f"[DEBUG] analyze_order_feasibility_with_ai: Client API key set: {hasattr(client, 'api_key')}")
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=[
                {"role": "system", "content": "You are an expert manufacturing operations AI consultant specializing in order feasibility analysis and supply chain optimization."},
                {"role": "user", "content": context}
            ],
            temperature=0.3,  # Lower temperature for more consistent, factual responses
            response_format={"type": "json_object"}
        )
        
        print(f"[DEBUG] analyze_order_feasibility_with_ai: API call successful!")
        ai_analysis = json.loads(response.choices[0].message.content)
        
        print(f"[DEBUG] analyze_order_feasibility_with_ai: Response parsed, recommendation: {ai_analysis.get('recommendation')}")
        
        return {
            "ai_enabled": True,
            "recommendation": ai_analysis.get("recommendation", "REVIEW_REQUIRED"),
            "confidence": ai_analysis.get("confidence", 50),
            "critical_bottleneck": ai_analysis.get("critical_bottleneck", "Unknown"),
            "actionable_recommendations": ai_analysis.get("actionable_recommendations", []),
            "alternative_strategies": ai_analysis.get("alternative_strategies", []),
            "executive_summary": ai_analysis.get("executive_summary", "AI analysis completed"),
            "model_used": "gpt-4-turbo-preview"
        }
        
    except Exception as e:
        print(f"[DEBUG] analyze_order_feasibility_with_ai: ERROR occurred: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"[DEBUG] analyze_order_feasibility_with_ai: Traceback:\n{traceback.format_exc()}")
        return _fallback_analysis(order_data, inventory_analysis, production_analysis, risk_analysis)


def _fallback_analysis(order_data, inventory_analysis, production_analysis, risk_analysis):
    """Fallback analysis when OpenAI is not available"""
    
    print(f"[DEBUG] _fallback_analysis: Using fallback (AI not available)")
    
    # Simple rule-based fallback
    has_inventory_issues = len(inventory_analysis.get('inventory_constraints', [])) > 0
    has_production_issues = len(production_analysis.get('production_constraints', [])) > 0
    high_risk = risk_analysis.get('overall_risk_score', 0) > 70
    
    if has_inventory_issues or has_production_issues or high_risk:
        recommendation = "NO-GO"
        confidence = 40
    else:
        recommendation = "GO"
        confidence = 75
    
    return {
        "ai_enabled": False,
        "recommendation": recommendation,
        "confidence": confidence,
        "critical_bottleneck": "Inventory shortage" if has_inventory_issues else "Production capacity" if has_production_issues else "Supply chain risks",
        "actionable_recommendations": [
            "Review component procurement schedule",
            "Consider alternative suppliers for critical components",
            "Optimize production line allocation"
        ],
        "alternative_strategies": [
            "Extend delivery timeline by 2 weeks",
            "Split order into multiple shipments",
            "Use premium expedited shipping for critical components"
        ],
        "executive_summary": f"Order feasibility analysis complete. {recommendation} recommended based on current constraints.",
        "model_used": "rule-based-fallback"
    }


def generate_risk_mitigation_strategies(risks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Use AI to generate intelligent risk mitigation strategies
    """
    
    print(f"[DEBUG] generate_risk_mitigation_strategies: Called with {len(risks) if risks else 0} risks")
    print(f"[DEBUG] generate_risk_mitigation_strategies: Client is None: {client is None}")
    
    if not client or not risks:
        print(f"[DEBUG] generate_risk_mitigation_strategies: Client or risks missing, returning fallback")
        return {
            "ai_enabled": False,
            "strategies": ["Increase safety stock", "Diversify suppliers", "Monitor situation closely"],
            "priority_actions": []
        }
    
    try:
        risk_summary = "\n".join([
            f"- {risk.get('risk_type', 'Unknown')}: {risk.get('description', 'No description')} "
            f"(Level: {risk.get('risk_level', 'Unknown')}, Region: {risk.get('region', 'Unknown')})"
            for risk in risks[:5]  # Top 5 risks
        ])
        
        prompt = f"""
You are a supply chain risk management AI expert. Analyze these supply chain risks and provide mitigation strategies:

ACTIVE RISKS:
{risk_summary}

Provide:
1. Top 3 priority mitigation actions (specific and actionable)
2. Contingency plans for each risk type
3. Early warning indicators to monitor
4. Estimated timeline for implementing mitigations

Format as JSON with keys: priority_actions, contingency_plans, early_warning_indicators, implementation_timeline
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Faster model for this task
            messages=[
                {"role": "system", "content": "You are a supply chain risk management expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        strategies = json.loads(response.choices[0].message.content)
        
        print(f"[DEBUG] generate_risk_mitigation_strategies: API call successful!")
        return {
            "ai_enabled": True,
            "priority_actions": strategies.get("priority_actions", []),
            "contingency_plans": strategies.get("contingency_plans", {}),
            "early_warning_indicators": strategies.get("early_warning_indicators", []),
            "implementation_timeline": strategies.get("implementation_timeline", "Unknown"),
            "model_used": "gpt-3.5-turbo"
        }
        
    except Exception as e:
        print(f"[DEBUG] generate_risk_mitigation_strategies: Exception occurred: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"[DEBUG] generate_risk_mitigation_strategies: Traceback:\n{traceback.format_exc()}")
        return {
            "ai_enabled": False,
            "strategies": ["Increase safety stock", "Diversify suppliers", "Monitor situation closely"],
            "priority_actions": [],
            "error": str(e)
        }


def predict_shipment_delay_probability(
    shipment_data: Dict[str, Any],
    weather_data: Optional[Dict[str, Any]] = None,
    logistics_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Use AI to predict probability of shipment delays based on multiple factors
    """
    
    if not client:
        # Simple fallback
        base_delay_prob = 15  # 15% base probability
        if weather_data and weather_data.get("severe_weather", False):
            base_delay_prob += 40
        if logistics_data and logistics_data.get("port_congestion", False):
            base_delay_prob += 30
        
        return {
            "ai_enabled": False,
            "delay_probability": min(base_delay_prob, 95),
            "expected_delay_days": 0 if base_delay_prob < 50 else 3,
            "confidence": 60
        }
    
    try:
        context = f"""
Analyze shipment delay probability:

SHIPMENT INFO:
- Origin: {shipment_data.get('origin', 'Unknown')}
- Destination: {shipment_data.get('destination', 'Unknown')}
- Transport method: {shipment_data.get('transport_method', 'Unknown')}
- Expected arrival: {shipment_data.get('expected_arrival', 'Unknown')}

WEATHER CONDITIONS:
{json.dumps(weather_data or {}, indent=2)}

LOGISTICS STATUS:
{json.dumps(logistics_data or {}, indent=2)}

Provide JSON with:
- delay_probability: number 0-100 (probability of delay)
- expected_delay_days: number (0 if no delay expected)
- primary_risk_factors: array of strings
- recommended_actions: array of strings
- confidence: number 0-100
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a logistics and supply chain AI analyst."},
                {"role": "user", "content": context}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        prediction = json.loads(response.choices[0].message.content)
        
        return {
            "ai_enabled": True,
            **prediction,
            "model_used": "gpt-3.5-turbo"
        }
        
    except Exception as e:
        print(f"Shipment delay prediction error: {e}")
        return {
            "ai_enabled": False,
            "delay_probability": 25,
            "expected_delay_days": 0,
            "confidence": 50
        }

