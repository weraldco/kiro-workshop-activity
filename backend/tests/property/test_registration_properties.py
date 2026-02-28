"""
Property-based tests for registration operations.

Tests verify that registration endpoints correctly handle status checks,
signup_enabled checks, and validation order across a wide range of test cases.
"""

import pytest
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
import json
import os
import tempfile

from app import create_app


# Strategies for generating test data
valid_statuses = st.sampled_from(['pending', 'ongoing', 'completed'])
non_pending_statuses = st.sampled_from(['ongoing', 'completed'])

# Email strategy that matches our simple validator pattern
# Pattern: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
simple_emails = st.builds(
    lambda local, domain, tld: f"{local}@{domain}.{tld}",
    local=st.text(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-', min_size=1, max_size=20).filter(lambda s: s[0].isalnum() if s else False),
    domain=st.text(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-', min_size=1, max_size=20).filter(lambda s: s[0].isalnum() if s else False),
    tld=st.text(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', min_size=2, max_size=6)
)


def create_test_client():
    """Create a test client with a temporary JSON file."""
    # Create a temporary file for testing
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    # Create app with test configuration
    app = create_app({'JSON_FILE_PATH': temp_path, 'TESTING': True})
    
    return app.test_client(), temp_path


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    participant_name=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
    participant_email=simple_emails
)
def test_property_7_registration_allowed_for_pending_workshops(participant_name, participant_email):
    """
    **Validates: Requirements 3.1**
    
    Feature: workshop-status-management-and-frontend, Property 7: Registration Allowed for Pending Workshops
    For any workshop with status="pending", signup_enabled=true, and available capacity,
    registration requests should succeed and return a 201 status.
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop with pending status
        workshop_data = {
            "title": "Test Workshop",
            "description": "Test description",
            "start_time": "2024-12-01T10:00:00",
            "end_time": "2024-12-01T12:00:00",
            "capacity": 10,
            "delivery_mode": "online"
        }
        
        create_response = client.post(
            '/api/workshop',
            data=json.dumps(workshop_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        workshop = json.loads(create_response.data)['data']
        workshop_id = workshop['id']
        
        # Verify workshop has pending status and signup_enabled=true by default
        assert workshop['status'] == 'pending', "Workshop should have pending status by default"
        assert workshop['signup_enabled'] is True, "Workshop should have signup_enabled=true by default"
        
        # Register a participant
        registration_data = {
            "participant_name": participant_name,
            "participant_email": participant_email
        }
        
        register_response = client.post(
            f'/api/workshop/{workshop_id}/register',
            data=json.dumps(registration_data),
            content_type='application/json'
        )
        
        # Verify registration succeeds
        assert register_response.status_code == 201, \
            f"Registration should succeed for pending workshop, got {register_response.status_code}"
        
        response_data = json.loads(register_response.data)
        assert response_data['success'] is True, "Response should indicate success"
        assert 'data' in response_data, "Response should contain registration data"
        
        registration = response_data['data']
        assert registration['participant_name'] == participant_name
        assert registration['participant_email'] == participant_email
        assert registration['workshop_id'] == workshop_id
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    status=non_pending_statuses,
    participant_name=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
    participant_email=simple_emails
)
def test_property_8_registration_blocked_for_non_pending_workshops(status, participant_name, participant_email):
    """
    **Validates: Requirements 3.2, 3.3**
    
    Feature: workshop-status-management-and-frontend, Property 8: Registration Blocked for Non-Pending Workshops
    For any workshop with status="ongoing" or status="completed", registration requests 
    should return a 403 status with a message indicating signups are closed.
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop
        workshop_data = {
            "title": "Test Workshop",
            "description": "Test description",
            "start_time": "2024-12-01T10:00:00",
            "end_time": "2024-12-01T12:00:00",
            "capacity": 10,
            "delivery_mode": "online"
        }
        
        create_response = client.post(
            '/api/workshop',
            data=json.dumps(workshop_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        workshop = json.loads(create_response.data)['data']
        workshop_id = workshop['id']
        
        # Update workshop status to non-pending
        status_response = client.patch(
            f'/api/workshop/{workshop_id}/status',
            data=json.dumps({"status": status}),
            content_type='application/json'
        )
        assert status_response.status_code == 200
        
        # Attempt to register a participant
        registration_data = {
            "participant_name": participant_name,
            "participant_email": participant_email
        }
        
        register_response = client.post(
            f'/api/workshop/{workshop_id}/register',
            data=json.dumps(registration_data),
            content_type='application/json'
        )
        
        # Verify registration is blocked
        assert register_response.status_code == 403, \
            f"Registration should be blocked for {status} workshop, got {register_response.status_code}"
        
        response_data = json.loads(register_response.data)
        assert response_data['success'] is False, "Response should indicate failure"
        assert 'error' in response_data, "Response should contain error message"
        
        error_message = response_data['error']
        assert 'closed' in error_message.lower(), \
            f"Error message should indicate signups are closed, got: {error_message}"
        
        # Verify correct message for each status
        if status == 'ongoing':
            assert 'ongoing' in error_message.lower(), \
                f"Error message should mention 'ongoing', got: {error_message}"
        elif status == 'completed':
            assert 'completed' in error_message.lower(), \
                f"Error message should mention 'completed', got: {error_message}"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    participant_name=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
    participant_email=simple_emails
)
def test_property_11_registration_blocked_when_signups_disabled(participant_name, participant_email):
    """
    **Validates: Requirements 5.1, 5.2**
    
    Feature: workshop-status-management-and-frontend, Property 11: Registration Blocked When Signups Disabled
    For any workshop with signup_enabled=false, registration requests should return a 403 status 
    with message "Signups are currently disabled for this workshop".
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop
        workshop_data = {
            "title": "Test Workshop",
            "description": "Test description",
            "start_time": "2024-12-01T10:00:00",
            "end_time": "2024-12-01T12:00:00",
            "capacity": 10,
            "delivery_mode": "online"
        }
        
        create_response = client.post(
            '/api/workshop',
            data=json.dumps(workshop_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        workshop = json.loads(create_response.data)['data']
        workshop_id = workshop['id']
        
        # Disable signups
        signup_response = client.patch(
            f'/api/workshop/{workshop_id}/signup',
            data=json.dumps({"signup_enabled": False}),
            content_type='application/json'
        )
        assert signup_response.status_code == 200
        
        # Attempt to register a participant
        registration_data = {
            "participant_name": participant_name,
            "participant_email": participant_email
        }
        
        register_response = client.post(
            f'/api/workshop/{workshop_id}/register',
            data=json.dumps(registration_data),
            content_type='application/json'
        )
        
        # Verify registration is blocked
        assert register_response.status_code == 403, \
            f"Registration should be blocked when signups disabled, got {register_response.status_code}"
        
        response_data = json.loads(register_response.data)
        assert response_data['success'] is False, "Response should indicate failure"
        assert 'error' in response_data, "Response should contain error message"
        
        error_message = response_data['error']
        assert error_message == "Signups are currently disabled for this workshop", \
            f"Expected exact error message, got: {error_message}"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    participant_name=st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
    participant_email=simple_emails
)
def test_property_12_registration_validation_order(participant_name, participant_email):
    """
    **Validates: Requirements 5.3, 3.4, 5.4**
    
    Feature: workshop-status-management-and-frontend, Property 12: Registration Validation Order
    For any workshop with signup_enabled=false and status="ongoing", registration requests 
    should return the signup_enabled error (403) rather than the status error, confirming 
    signup_enabled is checked first.
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop
        workshop_data = {
            "title": "Test Workshop",
            "description": "Test description",
            "start_time": "2024-12-01T10:00:00",
            "end_time": "2024-12-01T12:00:00",
            "capacity": 10,
            "delivery_mode": "online"
        }
        
        create_response = client.post(
            '/api/workshop',
            data=json.dumps(workshop_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        workshop = json.loads(create_response.data)['data']
        workshop_id = workshop['id']
        
        # Disable signups
        signup_response = client.patch(
            f'/api/workshop/{workshop_id}/signup',
            data=json.dumps({"signup_enabled": False}),
            content_type='application/json'
        )
        assert signup_response.status_code == 200
        
        # Set status to ongoing
        status_response = client.patch(
            f'/api/workshop/{workshop_id}/status',
            data=json.dumps({"status": "ongoing"}),
            content_type='application/json'
        )
        assert status_response.status_code == 200
        
        # Attempt to register a participant
        registration_data = {
            "participant_name": participant_name,
            "participant_email": participant_email
        }
        
        register_response = client.post(
            f'/api/workshop/{workshop_id}/register',
            data=json.dumps(registration_data),
            content_type='application/json'
        )
        
        # Verify registration is blocked with signup_enabled error (not status error)
        assert register_response.status_code == 403, \
            f"Registration should be blocked, got {register_response.status_code}"
        
        response_data = json.loads(register_response.data)
        assert response_data['success'] is False, "Response should indicate failure"
        assert 'error' in response_data, "Response should contain error message"
        
        error_message = response_data['error']
        # Should get signup_enabled error, not status error
        assert error_message == "Signups are currently disabled for this workshop", \
            f"Should get signup_enabled error first (validation order), got: {error_message}"
        assert 'ongoing' not in error_message.lower(), \
            f"Should not get status error when signup_enabled is false, got: {error_message}"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
