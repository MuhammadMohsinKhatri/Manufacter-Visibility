"""
Test Script for Weather Service
Tests the weather service functions directly without requiring the full API server.

Usage:
    python test_weather_service.py
"""

import os
import sys
from datetime import datetime

# Add backend to path so we can import the service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.weather_service import (
    get_weather_for_location,
    assess_weather_impact_on_shipment
)


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
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def test_get_weather_for_location():
    """Test get_weather_for_location function"""
    print_header("Test 1: Get Weather for Location")
    
    test_cases = [
        ("New York", "Normal location"),
        ("Southeast Asia", "High-risk location (simulated)"),
        ("London", "Normal location"),
        ("Gulf of Mexico", "High-risk location (simulated)"),
    ]
    
    results = []
    
    for location, description in test_cases:
        print(f"\n{Colors.BOLD}Testing: {location} - {description}{Colors.RESET}")
        try:
            result = get_weather_for_location(location, days_ahead=7)
            
            # Validate response structure
            required_fields = [
                "location", "data_source", "severe_weather", 
                "weather_risks", "overall_condition", "risk_score"
            ]
            
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print_error(f"Missing fields: {missing_fields}")
                results.append(False)
                continue
            
            # Print results
            print_success(f"Location: {result['location']}")
            print_info(f"Data Source: {result['data_source']}")
            print_info(f"Severe Weather: {result['severe_weather']}")
            print_info(f"Overall Condition: {result['overall_condition']}")
            print_info(f"Risk Score: {result['risk_score']}")
            
            if result['weather_risks']:
                print_warning(f"Weather Risks Found: {len(result['weather_risks'])}")
                for risk in result['weather_risks'][:2]:  # Show first 2
                    print(f"  - {risk.get('condition', 'Unknown')}: {risk.get('description', 'N/A')}")
            else:
                print_success("No weather risks detected")
            
            results.append(True)
            
        except Exception as e:
            print_error(f"Error testing {location}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    return all(results)


def test_assess_weather_impact():
    """Test assess_weather_impact_on_shipment function"""
    print_header("Test 2: Assess Weather Impact on Shipment")
    
    test_routes = [
        {
            "origin": "Shanghai",
            "destination": "Los Angeles",
            "route_type": "sea",
            "description": "Trans-Pacific sea route"
        },
        {
            "origin": "Southeast Asia",
            "destination": "New York",
            "route_type": "sea",
            "description": "High-risk route (simulated)"
        },
        {
            "origin": "London",
            "destination": "Paris",
            "route_type": "air",
            "description": "Short air route"
        },
    ]
    
    results = []
    
    for route in test_routes:
        print(f"\n{Colors.BOLD}Testing Route: {route['description']}{Colors.RESET}")
        print(f"  Origin: {route['origin']}")
        print(f"  Destination: {route['destination']}")
        print(f"  Route Type: {route['route_type']}")
        
        try:
            result = assess_weather_impact_on_shipment(
                origin=route['origin'],
                destination=route['destination'],
                route_type=route['route_type']
            )
            
            # Validate response structure
            required_fields = [
                "origin_weather", "destination_weather", "combined_risk_score",
                "delay_probability", "expected_delay_days", "severe_weather_detected",
                "recommendations", "assessment_time"
            ]
            
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print_error(f"Missing fields: {missing_fields}")
                results.append(False)
                continue
            
            # Print results
            print_success("Assessment completed")
            print_info(f"Combined Risk Score: {result['combined_risk_score']}/100")
            print_info(f"Delay Probability: {result['delay_probability']}%")
            print_info(f"Expected Delay Days: {result['expected_delay_days']}")
            print_info(f"Severe Weather Detected: {result['severe_weather_detected']}")
            
            if result['recommendations']:
                print_warning(f"Recommendations ({len(result['recommendations'])}):")
                for rec in result['recommendations'][:3]:  # Show first 3
                    print(f"  - {rec}")
            else:
                print_success("No recommendations (low risk)")
            
            # Show origin weather summary
            origin_weather = result.get('origin_weather', {})
            print_info(f"Origin Weather: {origin_weather.get('overall_condition', 'Unknown')} "
                      f"(Risk: {origin_weather.get('risk_score', 0)})")
            
            # Show destination weather summary
            dest_weather = result.get('destination_weather', {})
            print_info(f"Destination Weather: {dest_weather.get('overall_condition', 'Unknown')} "
                      f"(Risk: {dest_weather.get('risk_score', 0)})")
            
            results.append(True)
            
        except Exception as e:
            print_error(f"Error testing route: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    return all(results)


def check_api_key():
    """Check if OpenWeather API key is configured"""
    print_header("API Key Check")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        print_success("OpenWeatherMap API key found")
        print_info("Weather service will use REAL weather data")
        print_warning(f"API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
    else:
        print_warning("OpenWeatherMap API key NOT found")
        print_info("Weather service will use SIMULATED weather data")
        print_info("To use real weather data, set OPENWEATHER_API_KEY environment variable")
        print_info("Or add it to backend/.env file")
    
    return api_key is not None


def main():
    """Main test execution"""
    print_header("Weather Service Test Suite")
    print_info("Testing weather service functions")
    print_info(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check API key status
    has_api_key = check_api_key()
    
    # Run tests
    test1_passed = test_get_weather_for_location()
    test2_passed = test_assess_weather_impact()
    
    # Print summary
    print_header("Test Summary")
    
    if test1_passed:
        print_success("Test 1: get_weather_for_location() - PASSED")
    else:
        print_error("Test 1: get_weather_for_location() - FAILED")
    
    if test2_passed:
        print_success("Test 2: assess_weather_impact_on_shipment() - PASSED")
    else:
        print_error("Test 2: assess_weather_impact_on_shipment() - FAILED")
    
    if has_api_key:
        print_success("API Key: Configured (using real weather data)")
    else:
        print_warning("API Key: Not configured (using simulated data)")
    
    print()
    
    if test1_passed and test2_passed:
        print_success("All weather service tests passed! 🎉")
        return 0
    else:
        print_error("Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

