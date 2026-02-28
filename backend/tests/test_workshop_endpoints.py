"""
Tests for Workshop Endpoints with Authentication
"""
import pytest
import json
from app import create_app
from app.store.user_store import UserStore
from app.store.workshop_store_mysql import WorkshopStore
from app.auth import hash_password, generate_access_token
from app.database.connection import get_db_connection, close_db_connection


@pytest.fixture
def app():
    """Create test Flask app"""
    app = create_app({'TESTING': True})
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM participants")
        cursor.execute("DELETE FROM challenges")
        cursor.execute("DELETE FROM workshops")
        cursor.execute("DELETE FROM users")
        conn.commit()
    finally:
        cursor.close()
        close_db_connection(conn)
    yield


@pytest.fixture
def user_store():
    """Create user store"""
    return UserStore()


@pytest.fixture
def workshop_store():
    """Create workshop store"""
    return WorkshopStore()


@pytest.fixture
def test_user(user_store):
    """Create a test user"""
    password_hash = hash_password('TestPass123!')
    user = user_store.create_user('test@example.com', password_hash, 'Test User')
    return user


@pytest.fixture
def test_user2(user_store):
    """Create a second test user"""
    password_hash = hash_password('TestPass123!')
    user = user_store.create_user('test2@example.com', password_hash, 'Test User 2')
    return user


@pytest.fixture
def auth_token(test_user):
    """Generate auth token for test user"""
    return generate_access_token(
        user_id=test_user['id'],
        email=test_user['email'],
        name=test_user['name']
    )


@pytest.fixture
def auth_token2(test_user2):
    """Generate auth token for second test user"""
    return generate_access_token(
        user_id=test_user2['id'],
        email=test_user2['email'],
        name=test_user2['name']
    )


class TestCreateWorkshop:
    """Tests for POST /api/workshops"""
    
    def test_create_workshop_success(self, client, auth_token):
        """Test successful workshop creation"""
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({
                'title': 'Python Workshop',
                'description': 'Learn Python basics'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert 'id' in data
        assert data['title'] == 'Python Workshop'
        assert data['description'] == 'Learn Python basics'
        assert data['status'] == 'pending'
        assert data['signup_enabled'] is True
        assert 'owner_id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_create_workshop_without_auth(self, client):
        """Test workshop creation without authentication"""
        response = client.post('/api/workshops',
            data=json.dumps({
                'title': 'Python Workshop',
                'description': 'Learn Python basics'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_create_workshop_missing_title(self, client, auth_token):
        """Test workshop creation with missing title"""
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({
                'description': 'Learn Python basics'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'title' in data['error'].lower()
    
    def test_create_workshop_missing_description(self, client, auth_token):
        """Test workshop creation with missing description"""
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({
                'title': 'Python Workshop'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'description' in data['error'].lower()
    
    def test_create_workshop_title_too_long(self, client, auth_token):
        """Test workshop creation with title exceeding max length"""
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({
                'title': 'A' * 201,
                'description': 'Learn Python basics'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert '200' in data['error']


class TestListWorkshops:
    """Tests for GET /api/workshops"""
    
    def test_list_workshops_empty(self, client):
        """Test listing workshops when none exist"""
        response = client.get('/api/workshops')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_list_workshops_with_data(self, client, workshop_store, test_user):
        """Test listing workshops with data"""
        # Create workshops
        workshop_store.create_workshop('Workshop 1', 'Description 1', test_user['id'])
        workshop_store.create_workshop('Workshop 2', 'Description 2', test_user['id'])
        
        response = client.get('/api/workshops')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['title'] == 'Workshop 2'  # Most recent first
        assert data[1]['title'] == 'Workshop 1'
    
    def test_list_workshops_without_auth(self, client, workshop_store, test_user):
        """Test listing workshops without authentication (should work)"""
        workshop_store.create_workshop('Workshop 1', 'Description 1', test_user['id'])
        
        response = client.get('/api/workshops')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1


class TestGetMyWorkshops:
    """Tests for GET /api/workshops/my"""
    
    def test_get_my_workshops_success(self, client, workshop_store, test_user, auth_token):
        """Test getting current user's workshops"""
        # Create workshops for test user
        workshop_store.create_workshop('My Workshop 1', 'Description 1', test_user['id'])
        workshop_store.create_workshop('My Workshop 2', 'Description 2', test_user['id'])
        
        response = client.get('/api/workshops/my',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert all(w['owner_id'] == test_user['id'] for w in data)
    
    def test_get_my_workshops_empty(self, client, auth_token):
        """Test getting workshops when user has none"""
        response = client.get('/api/workshops/my',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_get_my_workshops_filters_by_owner(self, client, workshop_store, test_user, test_user2, auth_token):
        """Test that my workshops only returns current user's workshops"""
        # Create workshops for both users
        workshop_store.create_workshop('User 1 Workshop', 'Description 1', test_user['id'])
        workshop_store.create_workshop('User 2 Workshop', 'Description 2', test_user2['id'])
        
        response = client.get('/api/workshops/my',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == 'User 1 Workshop'
    
    def test_get_my_workshops_without_auth(self, client):
        """Test getting my workshops without authentication"""
        response = client.get('/api/workshops/my')
        
        assert response.status_code == 401


class TestGetWorkshop:
    """Tests for GET /api/workshops/<id>"""
    
    def test_get_workshop_success(self, client, workshop_store, test_user):
        """Test getting workshop by ID"""
        workshop = workshop_store.create_workshop('Test Workshop', 'Description', test_user['id'])
        
        response = client.get(f'/api/workshops/{workshop["id"]}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == workshop['id']
        assert data['title'] == 'Test Workshop'
    
    def test_get_workshop_not_found(self, client):
        """Test getting non-existent workshop"""
        response = client.get('/api/workshops/nonexistent-id')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['code'] == 'WORKSHOP_NOT_FOUND'


class TestUpdateWorkshop:
    """Tests for PATCH /api/workshops/<id>"""
    
    def test_update_workshop_title(self, client, workshop_store, test_user, auth_token):
        """Test updating workshop title"""
        workshop = workshop_store.create_workshop('Original Title', 'Description', test_user['id'])
        
        response = client.patch(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({'title': 'Updated Title'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
        assert data['description'] == 'Description'  # Unchanged
    
    def test_update_workshop_status(self, client, workshop_store, test_user, auth_token):
        """Test updating workshop status"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.patch(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({'status': 'ongoing'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ongoing'
    
    def test_update_workshop_signup_enabled(self, client, workshop_store, test_user, auth_token):
        """Test updating workshop signup_enabled"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.patch(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({'signup_enabled': False}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['signup_enabled'] is False
    
    def test_update_workshop_not_owner(self, client, workshop_store, test_user, test_user2, auth_token2):
        """Test updating workshop by non-owner"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.patch(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token2}'},
            data=json.dumps({'title': 'Hacked Title'}),
            content_type='application/json'
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['code'] == 'FORBIDDEN'
    
    def test_update_workshop_without_auth(self, client, workshop_store, test_user):
        """Test updating workshop without authentication"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.patch(f'/api/workshops/{workshop["id"]}',
            data=json.dumps({'title': 'Updated Title'}),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_update_workshop_not_found(self, client, auth_token):
        """Test updating non-existent workshop"""
        response = client.patch('/api/workshops/nonexistent-id',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({'title': 'Updated Title'}),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_update_workshop_invalid_status(self, client, workshop_store, test_user, auth_token):
        """Test updating workshop with invalid status"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.patch(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({'status': 'invalid'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestDeleteWorkshop:
    """Tests for DELETE /api/workshops/<id>"""
    
    def test_delete_workshop_success(self, client, workshop_store, test_user, auth_token):
        """Test deleting workshop"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.delete(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 204
        
        # Verify workshop is deleted
        deleted_workshop = workshop_store.get_workshop_by_id(workshop['id'])
        assert deleted_workshop is None
    
    def test_delete_workshop_not_owner(self, client, workshop_store, test_user, test_user2, auth_token2):
        """Test deleting workshop by non-owner"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.delete(f'/api/workshops/{workshop["id"]}',
            headers={'Authorization': f'Bearer {auth_token2}'}
        )
        
        assert response.status_code == 403
    
    def test_delete_workshop_without_auth(self, client, workshop_store, test_user):
        """Test deleting workshop without authentication"""
        workshop = workshop_store.create_workshop('Title', 'Description', test_user['id'])
        
        response = client.delete(f'/api/workshops/{workshop["id"]}')
        
        assert response.status_code == 401
    
    def test_delete_workshop_not_found(self, client, auth_token):
        """Test deleting non-existent workshop"""
        response = client.delete('/api/workshops/nonexistent-id',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 404


class TestWorkshopIntegration:
    """Integration tests for workshop workflows"""
    
    def test_full_workshop_lifecycle(self, client, auth_token):
        """Test complete workshop lifecycle: create → update → delete"""
        # Create workshop
        create_response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({
                'title': 'Lifecycle Workshop',
                'description': 'Testing full lifecycle'
            }),
            content_type='application/json'
        )
        
        assert create_response.status_code == 201
        workshop = json.loads(create_response.data)
        workshop_id = workshop['id']
        
        # Get workshop
        get_response = client.get(f'/api/workshops/{workshop_id}')
        assert get_response.status_code == 200
        
        # Update workshop
        update_response = client.patch(f'/api/workshops/{workshop_id}',
            headers={'Authorization': f'Bearer {auth_token}'},
            data=json.dumps({'status': 'ongoing'}),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        
        # Delete workshop
        delete_response = client.delete(f'/api/workshops/{workshop_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert delete_response.status_code == 204
        
        # Verify deleted
        get_after_delete = client.get(f'/api/workshops/{workshop_id}')
        assert get_after_delete.status_code == 404
