#!/usr/bin/env python
"""
Manual API testing script to verify all endpoints work correctly
"""
import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:3535/api/workshop"

def test_create_workshop():
    """Test POST /api/workshop"""
    print("\n1. Testing CREATE WORKSHOP...")
    start_time = datetime.now() + timedelta(days=7)
    end_time = start_time + timedelta(hours=6)
    
    data = {
        "title": "Python Workshop",
        "description": "Learn Python basics",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "capacity": 20,
        "delivery_mode": "online"
    }
    
    response = requests.post(BASE_URL, json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()['data']['id']
    return None

def test_list_workshops():
    """Test GET /api/workshop"""
    print("\n2. Testing LIST WORKSHOPS...")
    response = requests.get(BASE_URL)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Found {len(result['data'])} workshops")
    return result['data']

def test_get_workshop(workshop_id):
    """Test GET /api/workshop/{id}"""
    print(f"\n3. Testing GET WORKSHOP by ID...")
    response = requests.get(f"{BASE_URL}/{workshop_id}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")

def test_create_challenge(workshop_id):
    """Test POST /api/workshop/{id}/challenge"""
    print(f"\n4. Testing CREATE CHALLENGE...")
    data = {
        "title": "Build a Calculator",
        "description": "Create a simple calculator app"
    }
    
    response = requests.post(f"{BASE_URL}/{workshop_id}/challenge", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")

def test_register_participant(workshop_id):
    """Test POST /api/workshop/{id}/register"""
    print(f"\n5. Testing REGISTER PARTICIPANT...")
    data = {
        "participant_name": "John Doe",
        "participant_email": "john@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/{workshop_id}/register", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")

def test_list_registrations():
    """Test GET /api/workshop/registrations"""
    print(f"\n6. Testing LIST REGISTRATIONS...")
    response = requests.get(f"{BASE_URL}/registrations")
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Found {len(result['data'])} registrations")

def test_error_cases():
    """Test error handling"""
    print(f"\n7. Testing ERROR CASES...")
    
    # Test 404 - non-existent workshop
    print("   7a. Testing 404 for non-existent workshop...")
    response = requests.get(f"{BASE_URL}/non-existent-id")
    print(f"      Status: {response.status_code} (expected 404)")
    
    # Test 400 - invalid data
    print("   7b. Testing 400 for invalid data...")
    response = requests.post(BASE_URL, json={"title": ""})
    print(f"      Status: {response.status_code} (expected 400)")

if __name__ == "__main__":
    print("=" * 60)
    print("WORKSHOP MANAGEMENT API - MANUAL TESTING")
    print("=" * 60)
    
    try:
        # Test all endpoints
        workshop_id = test_create_workshop()
        
        if workshop_id:
            test_list_workshops()
            test_get_workshop(workshop_id)
            test_create_challenge(workshop_id)
            test_register_participant(workshop_id)
            test_list_registrations()
            test_error_cases()
            
            print("\n" + "=" * 60)
            print("✓ ALL MANUAL TESTS COMPLETED SUCCESSFULLY")
            print("=" * 60)
        else:
            print("\n✗ Failed to create workshop")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to API server")
        print("   Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
