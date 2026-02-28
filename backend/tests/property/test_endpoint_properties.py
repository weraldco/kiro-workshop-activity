"""
Property-based tests for API endpoint operations.

Tests verify that API endpoints correctly handle status updates, signup toggles,
and non-existent workshop scenarios across a wide range of generated test cases.
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
valid_signup_enabled = st.booleans()


def create_test_client():
    """Create a test client with a temporary JSON file."""
    # Create a temporary file for testing
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    # Create app with test configuration
    app = create_app({'JSON_FILE_PATH': temp_path, 'TESTING': True})
    
    return app.test_client(), temp_path


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(status=valid_statuses)
def test_property_5_status_update_operation(status):
    """
    **Validates: Requirements 2.1**
    
    Feature: workshop-status-management-and-frontend, Property 5: Status Update Operation
    For any existing workshop and valid status value ("pending", "ongoing", or "completed"),
    updating the workshop status should return a 200 status with the updated workshop 
    containing the new status value.
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop first
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
        
        # Update the workshop status
        update_response = client.patch(
            f'/api/workshop/{workshop_id}/status',
            data=json.dumps({"status": status}),
            content_type='application/json'
        )
        
        # Verify response
        assert update_response.status_code == 200, \
            f"Status update should return 200, got {update_response.status_code}"
        
        response_data = json.loads(update_response.data)
        assert response_data['success'] is True, "Response should indicate success"
        
        updated_workshop = response_data['data']
        assert updated_workshop['status'] == status, \
            f"Workshop status should be updated to '{status}', got '{updated_workshop['status']}'"
        assert updated_workshop['id'] == workshop_id, "Workshop ID should remain unchanged"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(signup_enabled=valid_signup_enabled)
def test_property_9_signup_enabled_update_operation(signup_enabled):
    """
    **Validates: Requirements 4.2**
    
    Feature: workshop-status-management-and-frontend, Property 9: Signup Enabled Flag Update Operation
    For any existing workshop and boolean value (true or false), updating the signup_enabled 
    flag should return a 200 status with the updated workshop containing the new signup_enabled value.
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop first
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
        
        # Update the signup_enabled flag
        update_response = client.patch(
            f'/api/workshop/{workshop_id}/signup',
            data=json.dumps({"signup_enabled": signup_enabled}),
            content_type='application/json'
        )
        
        # Verify response
        assert update_response.status_code == 200, \
            f"Signup update should return 200, got {update_response.status_code}"
        
        response_data = json.loads(update_response.data)
        assert response_data['success'] is True, "Response should indicate success"
        
        updated_workshop = response_data['data']
        assert updated_workshop['signup_enabled'] == signup_enabled, \
            f"Workshop signup_enabled should be updated to {signup_enabled}, got {updated_workshop['signup_enabled']}"
        assert updated_workshop['id'] == workshop_id, "Workshop ID should remain unchanged"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    endpoint_type=st.sampled_from(['status', 'signup']),
    workshop_id=st.text(min_size=1, max_size=50).filter(
        lambda s: s.strip() and '?' not in s and '/' not in s and '#' not in s
    )
)
def test_property_6_nonexistent_workshop_returns_404(endpoint_type, workshop_id):
    """
    **Validates: Requirements 2.3, 4.3, 6.6**
    
    Feature: workshop-status-management-and-frontend, Property 6: Non-Existent Workshop Returns 404
    For any request to update workshop status, update signup enabled, or retrieve challenges,
    if the workshop ID does not exist, the API should return a 404 status with an appropriate 
    error message.
    """
    client, temp_path = create_test_client()
    
    try:
        # Prepare request data based on endpoint type
        if endpoint_type == 'status':
            endpoint = f'/api/workshop/{workshop_id}/status'
            request_data = {"status": "pending"}
        else:  # signup
            endpoint = f'/api/workshop/{workshop_id}/signup'
            request_data = {"signup_enabled": True}
        
        # Make request to non-existent workshop
        response = client.patch(
            endpoint,
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # Verify response
        assert response.status_code == 404, \
            f"Request to non-existent workshop should return 404, got {response.status_code}"
        
        response_data = json.loads(response.data)
        assert response_data['success'] is False, "Response should indicate failure"
        assert 'error' in response_data, "Response should contain error message"
        assert 'does not exist' in response_data['error'].lower() or 'not found' in response_data['error'].lower(), \
            f"Error message should indicate workshop doesn't exist, got: {response_data['error']}"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)



@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    num_workshops=st.integers(min_value=0, max_value=10),
    workshop_status=valid_statuses,
    signup_enabled=valid_signup_enabled
)
def test_property_4_complete_workshop_data_in_responses(num_workshops, workshop_status, signup_enabled):
    """
    **Validates: Requirements 1.4, 10.2**
    
    Feature: workshop-status-management-and-frontend, Property 4: Complete Workshop Data in Responses
    For any workshop retrieved individually or in a list, the response should include all fields:
    id, title, description, start_time, end_time, capacity, delivery_mode, registration_count, 
    status, and signup_enabled.
    """
    client, temp_path = create_test_client()
    
    try:
        workshop_ids = []
        
        # Create multiple workshops with varying properties
        for i in range(num_workshops):
            workshop_data = {
                "title": f"Test Workshop {i}",
                "description": f"Test description {i}",
                "start_time": "2024-12-01T10:00:00",
                "end_time": "2024-12-01T12:00:00",
                "capacity": 10 + i,
                "delivery_mode": "online"
            }
            
            create_response = client.post(
                '/api/workshop',
                data=json.dumps(workshop_data),
                content_type='application/json'
            )
            assert create_response.status_code == 201
            workshop = json.loads(create_response.data)['data']
            workshop_ids.append(workshop['id'])
            
            # Update status and signup_enabled to test values
            client.patch(
                f'/api/workshop/{workshop["id"]}/status',
                data=json.dumps({"status": workshop_status}),
                content_type='application/json'
            )
            client.patch(
                f'/api/workshop/{workshop["id"]}/signup',
                data=json.dumps({"signup_enabled": signup_enabled}),
                content_type='application/json'
            )
        
        # Test 1: List all workshops endpoint
        list_response = client.get('/api/workshop')
        assert list_response.status_code == 200, \
            f"List workshops should return 200, got {list_response.status_code}"
        
        list_data = json.loads(list_response.data)
        assert list_data['success'] is True, "Response should indicate success"
        workshops = list_data['data']
        
        # Verify all workshops in list have complete data
        required_fields = [
            'id', 'title', 'description', 'start_time', 'end_time', 
            'capacity', 'delivery_mode', 'registration_count', 'status', 'signup_enabled'
        ]
        
        for workshop in workshops:
            for field in required_fields:
                assert field in workshop, \
                    f"Workshop in list should contain '{field}' field, got fields: {list(workshop.keys())}"
            
            # Verify field types
            assert isinstance(workshop['id'], str), "id should be a string"
            assert isinstance(workshop['title'], str), "title should be a string"
            assert isinstance(workshop['description'], str), "description should be a string"
            assert isinstance(workshop['start_time'], str), "start_time should be a string"
            assert isinstance(workshop['end_time'], str), "end_time should be a string"
            assert isinstance(workshop['capacity'], int), "capacity should be an integer"
            assert isinstance(workshop['delivery_mode'], str), "delivery_mode should be a string"
            assert isinstance(workshop['registration_count'], int), "registration_count should be an integer"
            assert isinstance(workshop['status'], str), "status should be a string"
            assert isinstance(workshop['signup_enabled'], bool), "signup_enabled should be a boolean"
            
            # Verify status is valid
            assert workshop['status'] in ['pending', 'ongoing', 'completed'], \
                f"status should be one of pending/ongoing/completed, got {workshop['status']}"
        
        # Test 2: Individual workshop retrieval
        for workshop_id in workshop_ids:
            get_response = client.get(f'/api/workshop/{workshop_id}')
            assert get_response.status_code == 200, \
                f"Get workshop should return 200, got {get_response.status_code}"
            
            get_data = json.loads(get_response.data)
            assert get_data['success'] is True, "Response should indicate success"
            workshop = get_data['data']
            
            # Verify individual workshop has complete data
            for field in required_fields:
                assert field in workshop, \
                    f"Individual workshop should contain '{field}' field, got fields: {list(workshop.keys())}"
            
            # Verify field types
            assert isinstance(workshop['id'], str), "id should be a string"
            assert isinstance(workshop['title'], str), "title should be a string"
            assert isinstance(workshop['description'], str), "description should be a string"
            assert isinstance(workshop['start_time'], str), "start_time should be a string"
            assert isinstance(workshop['end_time'], str), "end_time should be a string"
            assert isinstance(workshop['capacity'], int), "capacity should be an integer"
            assert isinstance(workshop['delivery_mode'], str), "delivery_mode should be a string"
            assert isinstance(workshop['registration_count'], int), "registration_count should be an integer"
            assert isinstance(workshop['status'], str), "status should be a string"
            assert isinstance(workshop['signup_enabled'], bool), "signup_enabled should be a boolean"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)



@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    endpoint_type=st.sampled_from([
        'create_workshop',
        'list_workshops',
        'get_workshop',
        'create_challenge',
        'register',
        'list_registrations',
        'update_status',
        'update_signup',
        'get_challenges'
    ])
)
def test_property_22_api_base_path_structure(endpoint_type):
    """
    **Validates: Requirements 14.1**
    
    Feature: workshop-status-management-and-frontend, Property 22: API Base Path Structure
    For any workshop-related endpoint, the URL path should start with "/api/workshop".
    """
    client, temp_path = create_test_client()
    
    try:
        # Create a workshop for endpoints that need it
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
        workshop_id = json.loads(create_response.data)['data']['id'] if create_response.status_code == 201 else 'test-id'
        
        # Map endpoint types to their paths and methods
        endpoint_configs = {
            'create_workshop': {
                'path': '/api/workshop',
                'method': 'POST',
                'data': workshop_data
            },
            'list_workshops': {
                'path': '/api/workshop',
                'method': 'GET',
                'data': None
            },
            'get_workshop': {
                'path': f'/api/workshop/{workshop_id}',
                'method': 'GET',
                'data': None
            },
            'create_challenge': {
                'path': f'/api/workshop/{workshop_id}/challenge',
                'method': 'POST',
                'data': {
                    'title': 'Test Challenge',
                    'description': 'Test description',
                    'html_content': '<p>Test</p>'
                }
            },
            'register': {
                'path': f'/api/workshop/{workshop_id}/register',
                'method': 'POST',
                'data': {
                    'participant_name': 'Test User',
                    'participant_email': 'test@example.com'
                }
            },
            'list_registrations': {
                'path': '/api/workshop/registrations',
                'method': 'GET',
                'data': None
            },
            'update_status': {
                'path': f'/api/workshop/{workshop_id}/status',
                'method': 'PATCH',
                'data': {'status': 'pending'}
            },
            'update_signup': {
                'path': f'/api/workshop/{workshop_id}/signup',
                'method': 'PATCH',
                'data': {'signup_enabled': True}
            },
            'get_challenges': {
                'path': f'/api/workshop/{workshop_id}/challenges?email=test@example.com',
                'method': 'GET',
                'data': None
            }
        }
        
        config = endpoint_configs[endpoint_type]
        path = config['path']
        
        # Verify the path starts with /api/workshop
        assert path.startswith('/api/workshop'), \
            f"Endpoint path '{path}' should start with '/api/workshop'"
        
        # Make the actual request to verify the endpoint exists and uses the correct path
        if config['method'] == 'GET':
            response = client.get(path)
        elif config['method'] == 'POST':
            response = client.post(
                path,
                data=json.dumps(config['data']),
                content_type='application/json'
            )
        elif config['method'] == 'PATCH':
            response = client.patch(
                path,
                data=json.dumps(config['data']),
                content_type='application/json'
            )
        
        # Verify the endpoint responds (not 404 for undefined endpoint)
        # We accept any status code except 404 (which would indicate the endpoint doesn't exist)
        assert response.status_code != 404 or 'does not exist' in json.loads(response.data).get('error', '').lower(), \
            f"Endpoint '{path}' should exist and respond (got {response.status_code})"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)



@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    endpoint_type=st.sampled_from([
        'create_workshop',
        'list_workshops',
        'get_workshop',
        'create_challenge',
        'register'
    ]),
    has_old_data=st.booleans()
)
def test_property_23_backward_compatibility_with_existing_endpoints(endpoint_type, has_old_data):
    """
    **Validates: Requirements 14.2**
    
    Feature: workshop-status-management-and-frontend, Property 23: Backward Compatibility with Existing Endpoints
    For any existing endpoint from the original workshop management API, the endpoint should 
    continue to function correctly with the same request/response format.
    """
    # Create a temporary file for testing
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    try:
        # If testing with old data, write old format data to the file
        if has_old_data:
            from datetime import datetime, timedelta
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
        client = app.test_client()
        
        # Test the endpoint based on type
        if endpoint_type == 'create_workshop':
            # Test POST /api/workshop
            workshop_data = {
                "title": "New Workshop",
                "description": "Test description",
                "start_time": "2024-12-01T10:00:00",
                "end_time": "2024-12-01T12:00:00",
                "capacity": 10,
                "delivery_mode": "online"
            }
            
            response = client.post(
                '/api/workshop',
                data=json.dumps(workshop_data),
                content_type='application/json'
            )
            
            # Verify response format
            assert response.status_code == 201, \
                f"Create workshop should return 201, got {response.status_code}"
            
            data = json.loads(response.data)
            assert 'success' in data, "Response should have 'success' field"
            assert 'data' in data, "Response should have 'data' field"
            assert data['success'] is True, "Response should indicate success"
            assert 'id' in data['data'], "Workshop data should have 'id' field"
            assert data['data']['title'] == workshop_data['title'], "Title should match"
            
            # Verify new fields are present with defaults
            assert 'status' in data['data'], "Workshop should have 'status' field"
            assert 'signup_enabled' in data['data'], "Workshop should have 'signup_enabled' field"
            assert data['data']['status'] == 'pending', "Default status should be 'pending'"
            assert data['data']['signup_enabled'] is True, "Default signup_enabled should be True"
        
        elif endpoint_type == 'list_workshops':
            # Test GET /api/workshop
            response = client.get('/api/workshop')
            
            # Verify response format
            assert response.status_code == 200, \
                f"List workshops should return 200, got {response.status_code}"
            
            data = json.loads(response.data)
            assert 'success' in data, "Response should have 'success' field"
            assert 'data' in data, "Response should have 'data' field"
            assert data['success'] is True, "Response should indicate success"
            assert isinstance(data['data'], list), "Data should be a list"
            
            # If old data exists, verify it's returned with defaults
            if has_old_data:
                assert len(data['data']) >= 1, "Should return at least the old workshop"
                old_workshop = next((w for w in data['data'] if w['id'] == 'old-workshop-1'), None)
                assert old_workshop is not None, "Old workshop should be in the list"
                assert 'status' in old_workshop, "Old workshop should have 'status' field"
                assert 'signup_enabled' in old_workshop, "Old workshop should have 'signup_enabled' field"
                assert old_workshop['status'] == 'pending', "Default status should be 'pending'"
                assert old_workshop['signup_enabled'] is True, "Default signup_enabled should be True"
        
        elif endpoint_type == 'get_workshop':
            # Test GET /api/workshop/{id}
            if has_old_data:
                workshop_id = 'old-workshop-1'
            else:
                # Create a workshop first
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
                workshop_id = json.loads(create_response.data)['data']['id']
            
            response = client.get(f'/api/workshop/{workshop_id}')
            
            # Verify response format
            assert response.status_code == 200, \
                f"Get workshop should return 200, got {response.status_code}"
            
            data = json.loads(response.data)
            assert 'success' in data, "Response should have 'success' field"
            assert 'data' in data, "Response should have 'data' field"
            assert data['success'] is True, "Response should indicate success"
            assert isinstance(data['data'], dict), "Data should be a dictionary"
            assert data['data']['id'] == workshop_id, "Workshop ID should match"
            
            # Verify new fields are present
            assert 'status' in data['data'], "Workshop should have 'status' field"
            assert 'signup_enabled' in data['data'], "Workshop should have 'signup_enabled' field"
        
        elif endpoint_type == 'create_challenge':
            # Test POST /api/workshop/{id}/challenge
            if has_old_data:
                workshop_id = 'old-workshop-1'
            else:
                # Create a workshop first
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
                workshop_id = json.loads(create_response.data)['data']['id']
            
            challenge_data = {
                "title": "Test Challenge",
                "description": "Test description",
                "html_content": "<p>Test content</p>"
            }
            
            response = client.post(
                f'/api/workshop/{workshop_id}/challenge',
                data=json.dumps(challenge_data),
                content_type='application/json'
            )
            
            # Verify response format
            assert response.status_code == 201, \
                f"Create challenge should return 201, got {response.status_code}"
            
            data = json.loads(response.data)
            assert 'success' in data, "Response should have 'success' field"
            assert 'data' in data, "Response should have 'data' field"
            assert data['success'] is True, "Response should indicate success"
            assert 'id' in data['data'], "Challenge data should have 'id' field"
            assert data['data']['title'] == challenge_data['title'], "Title should match"
            assert 'html_content' in data['data'], "Challenge should have 'html_content' field"
        
        elif endpoint_type == 'register':
            # Test POST /api/workshop/{id}/register
            if has_old_data:
                workshop_id = 'old-workshop-1'
            else:
                # Create a workshop first
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
                workshop_id = json.loads(create_response.data)['data']['id']
            
            registration_data = {
                "participant_name": "Test User",
                "participant_email": "test@example.com"
            }
            
            response = client.post(
                f'/api/workshop/{workshop_id}/register',
                data=json.dumps(registration_data),
                content_type='application/json'
            )
            
            # Verify response format
            # Should succeed because default status is "pending" and signup_enabled is True
            assert response.status_code == 201, \
                f"Register participant should return 201, got {response.status_code}"
            
            data = json.loads(response.data)
            assert 'success' in data, "Response should have 'success' field"
            assert 'data' in data, "Response should have 'data' field"
            assert data['success'] is True, "Response should indicate success"
            assert 'id' in data['data'], "Registration data should have 'id' field"
            assert data['data']['participant_name'] == registration_data['participant_name'], "Name should match"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)



@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    undefined_path=st.text(min_size=1, max_size=50).filter(
        lambda s: s.strip() and 
        not s.startswith('/api/workshop') and
        '?' not in s and '#' not in s and
        not s.startswith('/')
    ),
    method=st.sampled_from(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
)
def test_property_24_undefined_endpoints_return_404(undefined_path, method):
    """
    **Validates: Requirements 14.3**
    
    Feature: workshop-status-management-and-frontend, Property 24: Undefined Endpoints Return 404
    For any request to an undefined API endpoint, the API should return a 404 status.
    """
    client, temp_path = create_test_client()
    
    try:
        # Construct an undefined endpoint path
        # Make sure it doesn't accidentally match a real endpoint
        undefined_endpoint = f'/api/{undefined_path}'
        
        # Make request based on method
        if method == 'GET':
            response = client.get(undefined_endpoint)
        elif method == 'POST':
            response = client.post(
                undefined_endpoint,
                data=json.dumps({}),
                content_type='application/json'
            )
        elif method == 'PATCH':
            response = client.patch(
                undefined_endpoint,
                data=json.dumps({}),
                content_type='application/json'
            )
        elif method == 'PUT':
            response = client.put(
                undefined_endpoint,
                data=json.dumps({}),
                content_type='application/json'
            )
        elif method == 'DELETE':
            response = client.delete(undefined_endpoint)
        
        # Verify response is 404
        assert response.status_code == 404, \
            f"Request to undefined endpoint '{undefined_endpoint}' should return 404, got {response.status_code}"
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
