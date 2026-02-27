#!/usr/bin/env python3
"""
Test script for challenge visibility controls.

This script tests the new GET /api/workshop/{id}/challenges endpoint
to verify that challenge visibility is properly controlled based on
enrollment and workshop status.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:3535"

def test_challenge_visibility():
    """Test challenge visibility controls."""
    
    print("=" * 60)
    print("Testing Challenge Visibility Controls")
    print("=" * 60)
    
    # 1. Create a workshop
    print("\n1. Creating a workshop...")
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    workshop_data = {
        "title": "Python Workshop",
        "description": "Learn Python basics",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "capacity": 10,
        "delivery_mode": "online"
    }
    
    response = requests.post(f"{BASE_URL}/api/workshop", json=workshop_data)
    assert response.status_code == 201, f"Failed to create workshop: {response.text}"
    workshop = response.json()["data"]
    workshop_id = workshop["id"]
    print(f"✓ Workshop created with ID: {workshop_id}")
    print(f"  Status: {workshop['status']}")
    
    # 2. Create a challenge
    print("\n2. Creating a challenge...")
    challenge_data = {
        "title": "Build a Calculator",
        "description": "Create a simple calculator",
        "html_content": "<h1>Calculator Challenge</h1><p>Build a calculator with basic operations.</p>"
    }
    
    response = requests.post(f"{BASE_URL}/api/workshop/{workshop_id}/challenge", json=challenge_data)
    assert response.status_code == 201, f"Failed to create challenge: {response.text}"
    challenge = response.json()["data"]
    print(f"✓ Challenge created with ID: {challenge['id']}")
    print(f"  Title: {challenge['title']}")
    print(f"  Has html_content: {'html_content' in challenge}")
    
    # 3. Register a participant
    print("\n3. Registering a participant...")
    registration_data = {
        "participant_name": "Alice Smith",
        "participant_email": "alice@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/api/workshop/{workshop_id}/register", json=registration_data)
    assert response.status_code == 201, f"Failed to register: {response.text}"
    print(f"✓ Participant registered: {registration_data['participant_email']}")
    
    # 4. Try to access challenges while workshop is pending (should fail)
    print("\n4. Trying to access challenges while workshop is pending...")
    response = requests.get(f"{BASE_URL}/api/workshop/{workshop_id}/challenges?email=alice@example.com")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    error_msg = response.json()["error"]
    print(f"✓ Access denied (as expected): {error_msg}")
    
    # 5. Update workshop status to ongoing
    print("\n5. Updating workshop status to 'ongoing'...")
    response = requests.patch(f"{BASE_URL}/api/workshop/{workshop_id}/status", json={"status": "ongoing"})
    assert response.status_code == 200, f"Failed to update status: {response.text}"
    print(f"✓ Workshop status updated to 'ongoing'")
    
    # 6. Access challenges as enrolled participant (should succeed)
    print("\n6. Accessing challenges as enrolled participant...")
    response = requests.get(f"{BASE_URL}/api/workshop/{workshop_id}/challenges?email=alice@example.com")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    challenges = response.json()["data"]
    print(f"✓ Challenges retrieved successfully!")
    print(f"  Number of challenges: {len(challenges)}")
    if challenges:
        print(f"  First challenge: {challenges[0]['title']}")
        print(f"  Has html_content: {'html_content' in challenges[0]}")
    
    # 7. Try to access challenges as non-enrolled participant (should fail)
    print("\n7. Trying to access challenges as non-enrolled participant...")
    response = requests.get(f"{BASE_URL}/api/workshop/{workshop_id}/challenges?email=bob@example.com")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    error_msg = response.json()["error"]
    print(f"✓ Access denied (as expected): {error_msg}")
    
    # 8. Update workshop status to completed
    print("\n8. Updating workshop status to 'completed'...")
    response = requests.patch(f"{BASE_URL}/api/workshop/{workshop_id}/status", json={"status": "completed"})
    assert response.status_code == 200, f"Failed to update status: {response.text}"
    print(f"✓ Workshop status updated to 'completed'")
    
    # 9. Try to access challenges after workshop is completed (should fail)
    print("\n9. Trying to access challenges after workshop is completed...")
    response = requests.get(f"{BASE_URL}/api/workshop/{workshop_id}/challenges?email=alice@example.com")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    error_msg = response.json()["error"]
    print(f"✓ Access denied (as expected): {error_msg}")
    
    # 10. Try to access challenges without email parameter (should fail)
    print("\n10. Trying to access challenges without email parameter...")
    response = requests.get(f"{BASE_URL}/api/workshop/{workshop_id}/challenges")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    error_msg = response.json()["error"]
    print(f"✓ Request rejected (as expected): {error_msg}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_challenge_visibility()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to {BASE_URL}")
        print("Make sure the Flask server is running: python app.py")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
