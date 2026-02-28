"""
Unit tests for backward compatibility with existing data.

Tests that the system handles old data format (workshops without status/signup_enabled)
and that existing endpoints continue to work with the same request/response format.
"""

import json
import os
import tempfile
import pytest
from datetime import datetime, timedelta

from app import create_app
from app.store.workshop_store import WorkshopStore


@pytest.fixture
def client_with_old_data():
    """Create a test client with old format workshop data (no status/signup_enabled)."""
    # Create a temporary file for testing
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    # Write old format data directly to the JSON file
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    old_format_data = {
        "workshops": [
            {
                "id": "old-workshop-1",
                "title": "Old Format Workshop",
                "description": "Workshop without status and signup_enabled fields",
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 20,
                "delivery_mode": "online",
                "registration_count": 0,
                "created_at": datetime.now().isoformat()
                # Note: status and signup_enabled are intentionally missing
            }
        ],
        "challenges": [],
        "registrations": []
    }
    
    with open(temp_path, 'w') as f:
        json.dump(old_format_data, f)
    
    # Create app with test configuration
    app = create_app({'JSON_FILE_PATH': temp_path, 'TESTING': True})
    
    with app.test_client() as client:
        yield client, temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_list_workshops_with_old_data(client_with_old_data):
    """Test that listing workshops with old data format applies default values."""
    client, _ = client_with_old_data
    
    response = client.get('/api/workshop')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 1
    
    workshop = data['data'][0]
    assert workshop['id'] == 'old-workshop-1'
    assert workshop['title'] == 'Old Format Workshop'
    # Verify default values are applied
    assert workshop['status'] == 'pending'
    assert workshop['signup_enabled'] is True


def test_get_workshop_with_old_data(client_with_old_data):
    """Test that getting a specific workshop with old data format applies default values."""
    client, _ = client_with_old_data
    
    response = client.get('/api/workshop/old-workshop-1')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    workshop = data['data']
    assert workshop['id'] == 'old-workshop-1'
    assert workshop['title'] == 'Old Format Workshop'
    # Verify default values are applied
    assert workshop['status'] == 'pending'
    assert workshop['signup_enabled'] is True


def test_register_for_old_format_workshop(client_with_old_data):
    """Test that registration works for workshops in old data format."""
    client, _ = client_with_old_data
    
    registration_data = {
        'participant_name': 'Test User',
        'participant_email': 'test@example.com'
    }
    
    response = client.post('/api/workshop/old-workshop-1/register',
                          data=json.dumps(registration_data),
                          content_type='application/json')
    
    # Should succeed because default status is "pending" and signup_enabled is True
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['participant_name'] == 'Test User'


def test_update_status_on_old_format_workshop(client_with_old_data):
    """Test that status updates work on workshops in old data format."""
    client, _ = client_with_old_data
    
    status_data = {
        'status': 'ongoing'
    }
    
    response = client.patch('/api/workshop/old-workshop-1/status',
                           data=json.dumps(status_data),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['status'] == 'ongoing'


def test_update_signup_on_old_format_workshop(client_with_old_data):
    """Test that signup_enabled updates work on workshops in old data format."""
    client, _ = client_with_old_data
    
    signup_data = {
        'signup_enabled': False
    }
    
    response = client.patch('/api/workshop/old-workshop-1/signup',
                           data=json.dumps(signup_data),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['signup_enabled'] is False


def test_default_values_persisted_after_update(client_with_old_data):
    """Test that default values are persisted to JSON after workshop is updated."""
    client, temp_path = client_with_old_data
    
    # Update the workshop status
    status_data = {
        'status': 'ongoing'
    }
    client.patch('/api/workshop/old-workshop-1/status',
                data=json.dumps(status_data),
                content_type='application/json')
    
    # Read the JSON file directly to verify persistence
    with open(temp_path, 'r') as f:
        file_data = json.load(f)
    
    workshop = file_data['workshops'][0]
    # Verify that default values are now persisted
    assert 'status' in workshop
    assert workshop['status'] == 'ongoing'
    assert 'signup_enabled' in workshop
    assert workshop['signup_enabled'] is True


def test_existing_endpoints_maintain_format(client_with_old_data):
    """Test that existing endpoints maintain their request/response format."""
    client, _ = client_with_old_data
    
    # Test POST /api/workshop - create new workshop
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    workshop_data = {
        'title': 'New Workshop',
        'description': 'Test workshop',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 10,
        'delivery_mode': 'online'
    }
    
    response = client.post('/api/workshop',
                          data=json.dumps(workshop_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert 'id' in data['data']
    
    # Verify response includes new fields with defaults
    assert data['data']['status'] == 'pending'
    assert data['data']['signup_enabled'] is True
    
    # Test GET /api/workshop - list workshops
    response = client.get('/api/workshop')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)
    
    # Test GET /api/workshop/{id} - get specific workshop
    response = client.get('/api/workshop/old-workshop-1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], dict)


def test_challenge_creation_with_old_workshop(client_with_old_data):
    """Test that challenge creation works with old format workshops."""
    client, _ = client_with_old_data
    
    challenge_data = {
        'title': 'Test Challenge',
        'description': 'Challenge description',
        'html_content': '<p>Challenge content</p>'
    }
    
    response = client.post('/api/workshop/old-workshop-1/challenge',
                          data=json.dumps(challenge_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['title'] == 'Test Challenge'
    assert data['data']['html_content'] == '<p>Challenge content</p>'
