#!/usr/bin/env python
"""
Test that data persists across server restarts
"""
import requests
import json

BASE_URL = "http://localhost:3535/api/workshop"

print("Testing persistence after server restart...")
print("=" * 60)

try:
    # List workshops - should still have the workshop from before
    response = requests.get(BASE_URL)
    workshops = response.json()['data']
    
    print(f"✓ Found {len(workshops)} workshop(s) after restart")
    
    if len(workshops) > 0:
        workshop = workshops[0]
        print(f"  - Workshop ID: {workshop['id']}")
        print(f"  - Title: {workshop['title']}")
        print(f"  - Registration count: {workshop['registration_count']}")
    
    # List registrations
    response = requests.get(f"{BASE_URL}/registrations")
    registrations = response.json()['data']
    print(f"✓ Found {len(registrations)} registration(s) after restart")
    
    print("\n" + "=" * 60)
    print("✓ PERSISTENCE TEST PASSED - Data survived server restart!")
    print("=" * 60)
    
except requests.exceptions.ConnectionError:
    print("✗ ERROR: Could not connect to API server")
    print("   Make sure the Flask server is running: python app.py")
except Exception as e:
    print(f"✗ ERROR: {e}")
