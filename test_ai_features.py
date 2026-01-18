"""
Comprehensive Test Script for AI Features in Manufacturing Visibility System

This script tests all AI-powered endpoints:
1. Order Feasibility Check (GPT-4)
2. Shipment Delay Prediction (GPT-3.5 + Weather API)
3. Supply Chain Risk Assessment (GPT-3.5)

Usage:
    python test_ai_features.py

Requirements:
    - Backend server running on http://localhost:8000
    - OpenAI API key configured (or tests will show fallback behavior)
    - OpenWeatherMap API key configured (optional, for shipment tests)
"""

import requests
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import sys


# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 60  # Increased timeout for AI API calls


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")


def print_test(test_name: str):
    """Print test name"""
    print(f"{Colors.BLUE}🧪 Testing: {test_name}{Colors.RESET}")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.RESET}")


def validate_response(response: requests.Response, expected_status: int = 200) -> bool:
    """Validate HTTP response"""
    if response.status_code != expected_status:
        print_error(f"Expected status {expected_status}, got {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    return True


def validate_ai_features(data: Dict[str, Any], feature_name: str) -> Dict[str, bool]:
    """Validate AI features in response"""
    results = {}
    
    if feature_name == "order_feasibility":
        results["has_ai_analysis"] = "ai_analysis" in data
        results["ai_enabled"] = data.get("ai_analysis", {}).get("ai_enabled", False) if results["has_ai_analysis"] else False
        results["has_recommendation"] = "ai_recommendation" in data
        results["has_actionable_recommendations"] = "actionable_recommendations" in data
        results["has_executive_summary"] = "executive_summary" in data
        results["has_critical_bottleneck"] = "critical_bottleneck" in data
        
    elif feature_name == "shipment_delay":
        results["has_weather_assessment"] = "weather_assessment" in data
        results["has_ai_prediction"] = "ai_prediction" in data
        results["ai_enabled"] = data.get("ai_prediction", {}).get("ai_enabled", False) if results["has_ai_prediction"] else False
        results["has_overall_delay_probability"] = "overall_delay_probability" in data
        results["has_recommendations"] = "recommendations" in data
        results["has_expected_delay_days"] = "expected_delay_days" in data
        
    elif feature_name == "risk_assessment":
        results["has_ai_mitigation"] = "ai_mitigation" in data
        results["ai_enabled"] = data.get("ai_mitigation", {}).get("ai_enabled", False) if results["has_ai_mitigation"] else False
        results["has_priority_actions"] = "priority_actions" in data
        results["has_contingency_plans"] = "contingency_plans" in data
        results["has_early_warning_indicators"] = "early_warning_indicators" in data
        
    return results


def test_order_feasibility() -> Dict[str, Any]:
    """Test Order Feasibility Check with AI"""
    print_test("Order Feasibility Check (AI-Enhanced)")
    
    test_cases = [
        {
            "name": "Standard Order",
            "payload": {
                "product_ids": [1, 2],
                "quantities": [10, 5],
                "requested_delivery_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            }
        },
        {
            "name": "Large Order",
            "payload": {
                "product_ids": [1],
                "quantities": [100],
                "requested_delivery_date": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()
            }
        },
        {
            "name": "Multiple Products",
            "payload": {
                "product_ids": [1, 2, 3, 4],
                "quantities": [5, 10, 15, 20],
                "requested_delivery_date": (datetime.now(timezone.utc) + timedelta(days=45)).isoformat()
            }
        }
    ]
    
    results = {"passed": 0, "failed": 0, "tests": []}
    
    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        print(f"  Payload: {json.dumps(test_case['payload'], indent=2)}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/orders/check-feasibility",
                json=test_case['payload'],
                timeout=TIMEOUT
            )
            
            if not validate_response(response):
                results["failed"] += 1
                results["tests"].append({
                    "name": test_case['name'],
                    "status": "FAILED",
                    "error": f"HTTP {response.status_code}"
                })
                continue
            
            data = response.json()
            
            # Validate required fields
            required_fields = ["feasible", "earliest_possible_date", "confidence_score", 
                             "inventory_constraints", "production_constraints", "risk_factors"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_error(f"  Missing required fields: {missing_fields}")
                results["failed"] += 1
                results["tests"].append({
                    "name": test_case['name'],
                    "status": "FAILED",
                    "error": f"Missing fields: {missing_fields}"
                })
                continue
            
            # Debug: Print actual response structure
            print(f"[DEBUG] Test: Response keys: {list(data.keys())}")
            if "ai_analysis" in data:
                print(f"[DEBUG] Test: ai_analysis keys: {list(data['ai_analysis'].keys())}")
                print(f"[DEBUG] Test: ai_analysis['ai_enabled']: {data['ai_analysis'].get('ai_enabled', 'NOT_FOUND')}")
            
            # Validate AI features
            ai_validation = validate_ai_features(data, "order_feasibility")
            print(f"[DEBUG] Test: ai_validation result: {ai_validation}")
            
            if ai_validation["ai_enabled"]:
                print_success(f"  AI Analysis: ENABLED (GPT-4)")
                print_info(f"    Recommendation: {data.get('ai_recommendation', 'N/A')}")
                print_info(f"    Critical Bottleneck: {data.get('critical_bottleneck', 'N/A')[:50]}...")
                print_info(f"    Actionable Recommendations: {len(data.get('actionable_recommendations', []))} items")
            else:
                print_warning(f"  AI Analysis: DISABLED (Fallback mode - check OPENAI_API_KEY)")
            
            # Print key results
            print_info(f"  Feasible: {data['feasible']}")
            print_info(f"  Confidence Score: {data['confidence_score']:.2f}%")
            print_info(f"  Earliest Possible Date: {data['earliest_possible_date']}")
            
            results["passed"] += 1
            results["tests"].append({
                "name": test_case['name'],
                "status": "PASSED",
                "ai_enabled": ai_validation["ai_enabled"],
                "feasible": data['feasible'],
                "confidence_score": data['confidence_score']
            })
            
        except requests.exceptions.RequestException as e:
            print_error(f"  Request failed: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": test_case['name'],
                "status": "FAILED",
                "error": str(e)
            })
        except Exception as e:
            print_error(f"  Unexpected error: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": test_case['name'],
                "status": "FAILED",
                "error": str(e)
            })
    
    return results


def test_shipment_delay_prediction() -> Dict[str, Any]:
    """Test Shipment Delay Prediction with AI"""
    print_test("Shipment Delay Prediction (AI-Enhanced)")
    
    # Test with common shipment IDs (will skip if not found)
    shipment_ids = [1, 2, 3]
    
    print_info(f"  Testing with shipment IDs: {shipment_ids}")
    print_info(f"  Note: Will skip shipments that don't exist")
    
    results = {"passed": 0, "failed": 0, "tests": []}
    
    for shipment_id in shipment_ids:
        print(f"\n  Testing Shipment ID: {shipment_id}")
        
        try:
            payload = {"shipment_id": shipment_id}
            
            response = requests.post(
                f"{BASE_URL}/shipment-tracking/predict-delay",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 404:
                print_warning(f"  Shipment {shipment_id} not found (skipping)")
                continue
                
            if not validate_response(response):
                results["failed"] += 1
                results["tests"].append({
                    "name": f"Shipment {shipment_id}",
                    "status": "FAILED",
                    "error": f"HTTP {response.status_code}"
                })
                continue
            
            data = response.json()
            
            # Validate required fields
            required_fields = ["shipment_id", "overall_delay_probability", "expected_delay_days", 
                             "recommendations", "weather_assessment", "ai_prediction"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_error(f"  Missing required fields: {missing_fields}")
                results["failed"] += 1
                results["tests"].append({
                    "name": f"Shipment {shipment_id}",
                    "status": "FAILED",
                    "error": f"Missing fields: {missing_fields}"
                })
                continue
            
            # Validate AI features
            ai_validation = validate_ai_features(data, "shipment_delay")
            
            if ai_validation["ai_enabled"]:
                print_success(f"  AI Prediction: ENABLED (GPT-3.5)")
                print_info(f"    Delay Probability: {data['ai_prediction'].get('delay_probability', 0)}%")
                print_info(f"    Expected Delay Days: {data['ai_prediction'].get('expected_delay_days', 0)}")
            else:
                print_warning(f"  AI Prediction: DISABLED (Fallback mode)")
            
            # Print key results
            print_info(f"  Overall Delay Probability: {data['overall_delay_probability']:.2f}%")
            print_info(f"  Expected Delay Days: {data['expected_delay_days']}")
            print_info(f"  Recommendations: {len(data['recommendations'])} items")
            
            results["passed"] += 1
            results["tests"].append({
                "name": f"Shipment {shipment_id}",
                "status": "PASSED",
                "ai_enabled": ai_validation["ai_enabled"],
                "delay_probability": data['overall_delay_probability'],
                "expected_delay_days": data['expected_delay_days']
            })
            
        except requests.exceptions.RequestException as e:
            print_error(f"  Request failed: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": f"Shipment {shipment_id}",
                "status": "FAILED",
                "error": str(e)
            })
        except Exception as e:
            print_error(f"  Unexpected error: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": f"Shipment {shipment_id}",
                "status": "FAILED",
                "error": str(e)
            })
    
    return results


def test_risk_assessment() -> Dict[str, Any]:
    """Test Supply Chain Risk Assessment with AI"""
    print_test("Supply Chain Risk Assessment (AI-Enhanced)")
    
    test_cases = [
        {
            "name": "General Risk Assessment",
            "payload": {
                "time_horizon_days": 30
            }
        },
        {
            "name": "Regional Risk Assessment",
            "payload": {
                "time_horizon_days": 60,
                "region": "Southeast Asia"
            }
        },
        {
            "name": "Component-Specific Risk Assessment",
            "payload": {
                "time_horizon_days": 30,
                "component_ids": [1, 2, 3]
            }
        }
    ]
    
    results = {"passed": 0, "failed": 0, "tests": []}
    
    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        print(f"  Payload: {json.dumps(test_case['payload'], indent=2)}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/supply-chain/assess-risks/",
                json=test_case['payload'],
                timeout=TIMEOUT
            )
            
            if not validate_response(response):
                results["failed"] += 1
                results["tests"].append({
                    "name": test_case['name'],
                    "status": "FAILED",
                    "error": f"HTTP {response.status_code}"
                })
                continue
            
            data = response.json()
            
            # Validate required fields
            required_fields = ["overall_risk_score", "risks", "affected_components", 
                             "affected_suppliers", "mitigation_suggestions"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_error(f"  Missing required fields: {missing_fields}")
                results["failed"] += 1
                results["tests"].append({
                    "name": test_case['name'],
                    "status": "FAILED",
                    "error": f"Missing fields: {missing_fields}"
                })
                continue
            
            # Debug: Print actual response structure for risk assessment
            print(f"[DEBUG] Test: Risk assessment response keys: {list(data.keys())}")
            if "ai_mitigation" in data:
                print(f"[DEBUG] Test: ai_mitigation keys: {list(data['ai_mitigation'].keys())}")
                print(f"[DEBUG] Test: ai_mitigation['ai_enabled']: {data['ai_mitigation'].get('ai_enabled', 'NOT_FOUND')}")
            
            # Validate AI features
            ai_validation = validate_ai_features(data, "risk_assessment")
            print(f"[DEBUG] Test: Risk assessment ai_validation result: {ai_validation}")
            
            if ai_validation["ai_enabled"]:
                print_success(f"  AI Mitigation: ENABLED (GPT-3.5)")
                if "priority_actions" in data:
                    print_info(f"    Priority Actions: {len(data['priority_actions'])} items")
                if "contingency_plans" in data:
                    print_info(f"    Contingency Plans: {len(data['contingency_plans'])} items")
            else:
                print_warning(f"  AI Mitigation: DISABLED (Fallback mode - check OPENAI_API_KEY)")
            
            # Print key results
            print_info(f"  Overall Risk Score: {data['overall_risk_score']:.2f}")
            print_info(f"  Active Risks: {len(data['risks'])}")
            print_info(f"  Affected Components: {len(data['affected_components'])}")
            print_info(f"  Affected Suppliers: {len(data['affected_suppliers'])}")
            print_info(f"  Mitigation Suggestions: {len(data['mitigation_suggestions'])}")
            
            results["passed"] += 1
            results["tests"].append({
                "name": test_case['name'],
                "status": "PASSED",
                "ai_enabled": ai_validation["ai_enabled"],
                "risk_score": data['overall_risk_score'],
                "active_risks": len(data['risks'])
            })
            
        except requests.exceptions.RequestException as e:
            print_error(f"  Request failed: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": test_case['name'],
                "status": "FAILED",
                "error": str(e)
            })
        except Exception as e:
            print_error(f"  Unexpected error: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": test_case['name'],
                "status": "FAILED",
                "error": str(e)
            })
    
    return results


def test_api_health() -> bool:
    """Test if API is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False


def print_summary(all_results: Dict[str, Dict[str, Any]]):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total_passed = sum(r["passed"] for r in all_results.values())
    total_failed = sum(r["failed"] for r in all_results.values())
    total_tests = total_passed + total_failed
    
    print(f"\n{Colors.BOLD}Overall Results:{Colors.RESET}")
    print(f"  Total Tests: {total_tests}")
    print(f"  {Colors.GREEN}Passed: {total_passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed: {total_failed}{Colors.RESET}")
    
    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        print(f"  Success Rate: {success_rate:.1f}%")
    
    print(f"\n{Colors.BOLD}Feature Breakdown:{Colors.RESET}")
    for feature, results in all_results.items():
        feature_name = feature.replace("_", " ").title()
        print(f"\n  {feature_name}:")
        print(f"    Passed: {results['passed']}")
        print(f"    Failed: {results['failed']}")
        
        # Count AI-enabled tests
        ai_enabled_count = sum(1 for test in results.get("tests", []) if test.get("ai_enabled", False))
        print(f"    AI-Enabled: {ai_enabled_count}/{results['passed']}")
    
    print()


def main():
    """Main test execution"""
    print_header("AI Features Test Suite")
    print_info("Testing all AI-powered endpoints in Manufacturing Visibility System")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Timeout: {TIMEOUT}s per request\n")
    
    # Check API health
    print_test("API Health Check")
    if not test_api_health():
        print_error("API is not accessible. Make sure backend server is running on http://localhost:8000")
        sys.exit(1)
    print_success("API is accessible\n")
    
    # Run all tests
    all_results = {}
    
    # Test 1: Order Feasibility
    all_results["order_feasibility"] = test_order_feasibility()
    
    # Test 2: Shipment Delay Prediction
    all_results["shipment_delay"] = test_shipment_delay_prediction()
    
    # Test 3: Risk Assessment
    all_results["risk_assessment"] = test_risk_assessment()
    
    # Print summary
    print_summary(all_results)
    
    # Exit with appropriate code
    total_failed = sum(r["failed"] for r in all_results.values())
    if total_failed > 0:
        sys.exit(1)
    else:
        print_success("All tests passed! 🎉")
        sys.exit(0)


if __name__ == "__main__":
    main()

