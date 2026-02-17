"""
Example: Testing Strava Insights API
Run this script to test the API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n📡 Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_root():
    """Test root endpoint"""
    print("\n📡 Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_enrich():
    """Test enrich endpoint"""
    print("\n📡 Testing /enrich endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/enrich", timeout=30)
        print(f"Status: {response.status_code}")
        data = response.json()

        if isinstance(data, list):
            print(f"✅ Received {len(data)} activities")
            if data:
                print(f"\n📋 First activity sample:")
                print(json.dumps(data[0], indent=2, default=str))
        else:
            print(f"Response: {json.dumps(data, indent=2)}")
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Make sure Java backend is running on http://localhost:8080")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Make sure FastAPI is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_insights():
    """Test insights endpoint"""
    print("\n🧠 Testing /insights endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/insights", timeout=30)
        print(f"Status: {response.status_code}")
        data = response.json()

        print("\n📊 Insights Summary:")
        if "summary" in data:
            for insight in data["summary"]:
                print(f"  • {insight}")

        print("\n🏃 Performance by Condition:")
        if "performance_by_condition" in data:
            for condition, stats in data["performance_by_condition"].items():
                print(f"  • {condition}: avg_pace={stats.get('avg_pace')} min/km (n={stats.get('count')})")

        print("\n🌡️ Best Conditions:")
        if "best_conditions" in data and data["best_conditions"]:
            bc = data["best_conditions"]
            print(f"  • Condition: {bc.get('condition')}")
            print(f"  • Average Pace: {bc.get('avg_pace')} min/km")
            print(f"  • Sample Size: {bc.get('count')} activities")

        print("\n💨 Wind Impact:")
        if "wind_impact" in data and data["wind_impact"]:
            wi = data["wind_impact"]
            print(f"  • Low Wind Avg Pace: {wi.get('avg_pace_low_wind')} min/km")
            print(f"  • High Wind Avg Pace: {wi.get('avg_pace_high_wind')} min/km")
            print(f"  • Wind Impact: {wi.get('impact_percent')}%")

        print(f"\n📊 Total Activities Analyzed: {data.get('total_activities_analyzed', 0)}")

    except requests.exceptions.Timeout:
        print("❌ Request timeout - Make sure Java backend is running on http://localhost:8080")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Make sure FastAPI is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("=" * 60)
    print("🏃 STRAVA INSIGHTS API - TEST SUITE")
    print("=" * 60)
    print(f"Testing at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    test_health()
    test_root()
    test_enrich()
    test_insights()

    print("\n" + "=" * 60)
    print("✅ Test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
