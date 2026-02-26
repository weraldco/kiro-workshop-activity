"""
Unit tests for workshop routes.

Tests specific examples and edge cases for the Flask API endpoints.
"""

import json
import os
import tempfile
import pytest
from datetime import datetime, timedelta

from app import create_app


@pytest.fixture
def client():
    """Create a test client with a temporary JSON file."""
    # Create a temporary file for testing
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    # Create app with test configuration
    app = create_app({'JSON_FILE_PATH': temp_path, 'TESTING': True})
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_create_workshop_success(client):
    """Test creating a workshop with valid data."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    workshop_data = {
        'title': 'Python Workshop',
        'description': 'Learn Python basics',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 20,
        'delivery_mode': 'online'
    }
    
    response = client.post('/api/workshop',
                          data=json.dumps(workshop_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'id' in data['data']
    assert data['data']['title'] == 'Python Workshop'
    assert data['data']['registration_count'] == 0


def test_create_workshop_empty_title(client):
    """Test creating a workshop with empty title returns 400."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    workshop_data = {
        'title': '',
        'description': 'Test',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 20,
        'delivery_mode': 'online'
    }
    
    response = client.post('/api/workshop',
                          data=json.dumps(workshop_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'title' in data['error'].lower()


def test_list_workshops_empty(client):
    """Test listing workshops when none exist."""
    response = client.get('/api/workshop')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data'] == []


def test_list_workshops_with_data(client):
    """Test listing workshops after creating some."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    # Create first workshop
    workshop_data1 = {
        'title': 'Workshop 1',
        'description': 'First workshop',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 10,
        'delivery_mode': 'online'
    }
    client.post('/api/workshop',
               data=json.dumps(workshop_data1),
               content_type='application/json')
    
    # Create second workshop
    workshop_data2 = {
        'title': 'Workshop 2',
        'description': 'Second workshop',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 15,
        'delivery_mode': 'face-to-face'
    }
    client.post('/api/workshop',
               data=json.dumps(workshop_data2),
               content_type='application/json')
    
    # List workshops
    response = client.get('/api/workshop')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 2


def test_get_workshop_by_id(client):
    """Test retrieving a specific workshop by ID."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    # Create workshop
    workshop_data = {
        'title': 'Test Workshop',
        'description': 'Test description',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 25,
        'delivery_mode': 'hybrid'
    }
    create_response = client.post('/api/workshop',
                                 data=json.dumps(workshop_data),
                                 content_type='application/json')
    created_data = json.loads(create_response.data)
    workshop_id = created_data['data']['id']
    
    # Get workshop by ID
    response = client.get(f'/api/workshop/{workshop_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['id'] == workshop_id
    assert data['data']['title'] == 'Test Workshop'


def test_get_workshop_not_found(client):
    """Test retrieving a non-existent workshop returns 404."""
    response = client.get('/api/workshop/non-existent-id')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'does not exist' in data['error']


def test_create_challenge_success(client):
    """Test creating a challenge for an existing workshop."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    # Create workshop first
    workshop_data = {
        'title': 'Workshop with Challenge',
        'description': 'Test',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 20,
        'delivery_mode': 'online'
    }
    create_response = client.post('/api/workshop',
                                 data=json.dumps(workshop_data),
                                 content_type='application/json')
    workshop_id = json.loads(create_response.data)['data']['id']
    
    # Create challenge
    challenge_data = {
        'title': 'Build a REST API',
        'description': 'Create a simple REST API using Flask'
    }
    response = client.post(f'/api/workshop/{workshop_id}/challenge',
                          data=json.dumps(challenge_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'id' in data['data']
    assert data['data']['title'] == 'Build a REST API'
    assert data['data']['workshop_id'] == workshop_id


def test_create_challenge_workshop_not_found(client):
    """Test creating a challenge for non-existent workshop returns 404."""
    challenge_data = {
        'title': 'Test Challenge',
        'description': 'Test'
    }
    response = client.post('/api/workshop/non-existent-id/challenge',
                          data=json.dumps(challenge_data),
                          content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False


def test_register_participant_success(client):
    """Test registering a participant for a workshop."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    # Create workshop first
    workshop_data = {
        'title': 'Workshop for Registration',
        'description': 'Test',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 5,
        'delivery_mode': 'online'
    }
    create_response = client.post('/api/workshop',
                                 data=json.dumps(workshop_data),
                                 content_type='application/json')
    workshop_id = json.loads(create_response.data)['data']['id']
    
    # Register participant
    registration_data = {
        'participant_name': 'John Doe',
        'participant_email': 'john@example.com'
    }
    response = client.post(f'/api/workshop/{workshop_id}/register',
                          data=json.dumps(registration_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'id' in data['data']
    assert data['data']['participant_name'] == 'John Doe'
    assert data['data']['workshop_id'] == workshop_id


def test_register_participant_workshop_full(client):
    """Test registering for a full workshop returns 409."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    # Create workshop with capacity of 1
    workshop_data = {
        'title': 'Small Workshop',
        'description': 'Test',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 1,
        'delivery_mode': 'online'
    }
    create_response = client.post('/api/workshop',
                                 data=json.dumps(workshop_data),
                                 content_type='application/json')
    workshop_id = json.loads(create_response.data)['data']['id']
    
    # Register first participant (should succeed)
    registration_data1 = {
        'participant_name': 'First Person',
        'participant_email': 'first@example.com'
    }
    client.post(f'/api/workshop/{workshop_id}/register',
               data=json.dumps(registration_data1),
               content_type='application/json')
    
    # Try to register second participant (should fail with 409)
    registration_data2 = {
        'participant_name': 'Second Person',
        'participant_email': 'second@example.com'
    }
    response = client.post(f'/api/workshop/{workshop_id}/register',
                          data=json.dumps(registration_data2),
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'full' in data['error'].lower()


def test_list_registrations_empty(client):
    """Test listing registrations when none exist."""
    response = client.get('/api/workshop/registrations')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data'] == []


def test_list_registrations_with_data(client):
    """Test listing registrations after creating some."""
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    # Create workshop
    workshop_data = {
        'title': 'Workshop',
        'description': 'Test',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': 10,
        'delivery_mode': 'online'
    }
    create_response = client.post('/api/workshop',
                                 data=json.dumps(workshop_data),
                                 content_type='application/json')
    workshop_id = json.loads(create_response.data)['data']['id']
    
    # Register two participants
    for i in range(2):
        registration_data = {
            'participant_name': f'Participant {i+1}',
            'participant_email': f'participant{i+1}@example.com'
        }
        client.post(f'/api/workshop/{workshop_id}/register',
                   data=json.dumps(registration_data),
                   content_type='application/json')
    
    # List registrations
    response = client.get('/api/workshop/registrations')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 2


def test_malformed_json(client):
    """Test that malformed JSON returns 400."""
    response = client.post('/api/workshop',
                          data='not valid json',
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_response_content_type(client):
    """Test that all responses have application/json content type."""
    response = client.get('/api/workshop')
    assert 'application/json' in response.content_type
