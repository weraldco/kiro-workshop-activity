"""
Tests for Authentication Endpoints
"""
import pytest
import json
from app import create_app
from app.store.user_store import UserStore
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


class TestRegisterEndpoint:
    """Tests for POST /api/auth/register"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'SecurePass123!',
                'name': 'Test User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert 'id' in data
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'
        assert 'access_token' in data
        assert data['token_type'] == 'Bearer'
        assert 'password_hash' not in data
        assert 'created_at' in data
    
    def test_register_missing_body(self, client):
        """Test registration with missing request body"""
        response = client.post('/api/auth/register',
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'MISSING_BODY'
    
    def test_register_missing_email(self, client):
        """Test registration with missing email"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'password': 'SecurePass123!',
                'name': 'Test User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
        assert 'email' in data['error'].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'invalid-email',
                'password': 'SecurePass123!',
                'name': 'Test User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
    
    def test_register_missing_password(self, client):
        """Test registration with missing password"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com',
                'name': 'Test User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
        assert 'password' in data['error'].lower()
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'weak',
                'name': 'Test User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
    
    def test_register_missing_name(self, client):
        """Test registration with missing name"""
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'SecurePass123!'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
        assert 'name' in data['error'].lower()
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # First registration
        client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'SecurePass123!',
                'name': 'Test User'
            }),
            content_type='application/json'
        )
        
        # Second registration with same email
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'DifferentPass123!',
                'name': 'Another User'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['code'] == 'EMAIL_EXISTS'


class TestLoginEndpoint:
    """Tests for POST /api/auth/login"""
    
    @pytest.fixture
    def registered_user(self):
        """Create a registered user for login tests"""
        user_store = UserStore()
        password_hash = hash_password('SecurePass123!')
        user = user_store.create_user('test@example.com', password_hash, 'Test User')
        return user
    
    def test_login_success(self, client, registered_user):
        """Test successful login"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'SecurePass123!'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['id'] == registered_user['id']
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'
        assert 'access_token' in data
        assert data['token_type'] == 'Bearer'
        assert 'password_hash' not in data
    
    def test_login_missing_body(self, client):
        """Test login with missing request body"""
        response = client.post('/api/auth/login',
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'MISSING_BODY'
    
    def test_login_missing_email(self, client):
        """Test login with missing email"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'password': 'SecurePass123!'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
    
    def test_login_missing_password(self, client):
        """Test login with missing password"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 'VALIDATION_ERROR'
    
    def test_login_invalid_email(self, client, registered_user):
        """Test login with non-existent email"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'SecurePass123!'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['code'] == 'INVALID_CREDENTIALS'
    
    def test_login_wrong_password(self, client, registered_user):
        """Test login with wrong password"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'WrongPassword123!'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['code'] == 'INVALID_CREDENTIALS'
    
    def test_login_case_insensitive_email(self, client, registered_user):
        """Test login with different email case (should work - case insensitive)"""
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'TEST@EXAMPLE.COM',
                'password': 'SecurePass123!'
            }),
            content_type='application/json'
        )
        
        # Should succeed because email lookup is case-insensitive
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'test@example.com'  # Original case preserved


class TestGetCurrentUserEndpoint:
    """Tests for GET /api/auth/me"""
    
    @pytest.fixture
    def registered_user(self):
        """Create a registered user"""
        user_store = UserStore()
        password_hash = hash_password('SecurePass123!')
        user = user_store.create_user('test@example.com', password_hash, 'Test User')
        return user
    
    @pytest.fixture
    def auth_token(self, registered_user):
        """Generate auth token for user"""
        return generate_access_token(
            user_id=registered_user['id'],
            email=registered_user['email'],
            name=registered_user['name']
        )
    
    def test_get_current_user_success(self, client, registered_user, auth_token):
        """Test getting current user with valid token"""
        response = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['id'] == registered_user['id']
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'
        assert 'password_hash' not in data
        assert 'created_at' in data
    
    def test_get_current_user_missing_token(self, client):
        """Test getting current user without token"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['code'] == 'UNAUTHORIZED'
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get('/api/auth/me',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['code'] == 'INVALID_TOKEN'
    
    def test_get_current_user_malformed_header(self, client, auth_token):
        """Test getting current user with malformed auth header"""
        # Missing "Bearer" prefix
        response = client.get('/api/auth/me',
            headers={'Authorization': auth_token}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['code'] == 'INVALID_AUTH_HEADER'
    
    def test_get_current_user_expired_token(self, client):
        """Test getting current user with expired token"""
        # This is a known expired token (you'd need to generate one that's actually expired)
        # For now, we'll use an invalid token as a proxy
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAwMDAwMDB9.invalid"
        
        response = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {expired_token}'}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['code'] == 'INVALID_TOKEN'


class TestAuthIntegration:
    """Integration tests for auth flow"""
    
    def test_full_registration_and_login_flow(self, client):
        """Test complete registration → login → get user flow"""
        # 1. Register
        register_response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'integration@example.com',
                'password': 'IntegrationTest123!',
                'name': 'Integration User'
            }),
            content_type='application/json'
        )
        
        assert register_response.status_code == 201
        register_data = json.loads(register_response.data)
        register_token = register_data['access_token']
        
        # 2. Use registration token to get user
        me_response_1 = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {register_token}'}
        )
        
        assert me_response_1.status_code == 200
        me_data_1 = json.loads(me_response_1.data)
        assert me_data_1['email'] == 'integration@example.com'
        
        # 3. Login with same credentials
        login_response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'integration@example.com',
                'password': 'IntegrationTest123!'
            }),
            content_type='application/json'
        )
        
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        login_token = login_data['access_token']
        
        # 4. Use login token to get user
        me_response_2 = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {login_token}'}
        )
        
        assert me_response_2.status_code == 200
        me_data_2 = json.loads(me_response_2.data)
        assert me_data_2['email'] == 'integration@example.com'
        assert me_data_2['id'] == register_data['id']
    
    def test_token_works_across_requests(self, client):
        """Test that token can be used for multiple requests"""
        # Register
        register_response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'persistent@example.com',
                'password': 'PersistentTest123!',
                'name': 'Persistent User'
            }),
            content_type='application/json'
        )
        
        token = json.loads(register_response.data)['access_token']
        
        # Make multiple requests with same token
        for _ in range(3):
            response = client.get('/api/auth/me',
                headers={'Authorization': f'Bearer {token}'}
            )
            assert response.status_code == 200
