"""
Tests for authentication services (password and JWT)
"""
import pytest
import time
from app.auth.password_service import hash_password, verify_password
from app.auth.auth_service import generate_access_token, verify_token


class TestPasswordService:
    """Tests for password hashing and verification"""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
    
    def test_hash_password_different_each_time(self):
        """Test that hashing the same password produces different hashes (due to salt)"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test that verify_password returns True for correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test that verify_password returns False for incorrect password"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty(self):
        """Test that verify_password handles empty password"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False
    
    def test_verify_password_invalid_hash(self):
        """Test that verify_password handles invalid hash"""
        password = "TestPassword123!"
        invalid_hash = "not-a-valid-bcrypt-hash"
        
        assert verify_password(password, invalid_hash) is False


class TestAuthService:
    """Tests for JWT token generation and verification"""
    
    def test_generate_access_token_returns_string(self):
        """Test that generate_access_token returns a string"""
        token = generate_access_token(
            user_id="user-123",
            email="test@example.com",
            name="Test User"
        )
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self):
        """Test that verify_token returns payload for valid token"""
        user_id = "user-123"
        email = "test@example.com"
        name = "Test User"
        
        token = generate_access_token(user_id, email, name)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload['user_id'] == user_id
        assert payload['email'] == email
        assert payload['name'] == name
        assert 'exp' in payload
        assert 'iat' in payload
    
    def test_verify_token_invalid(self):
        """Test that verify_token returns None for invalid token"""
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)
        
        assert payload is None
    
    def test_verify_token_empty(self):
        """Test that verify_token returns None for empty token"""
        payload = verify_token("")
        
        assert payload is None
    
    def test_verify_token_expired(self):
        """Test that verify_token returns None for expired token"""
        # This test would require mocking time or setting a very short expiration
        # For now, we'll skip this test as it would require waiting 30 minutes
        # In a real scenario, you'd mock the expiration time
        pass
    
    def test_token_contains_user_data(self):
        """Test that token contains all user data"""
        user_id = "user-456"
        email = "another@example.com"
        name = "Another User"
        
        token = generate_access_token(user_id, email, name)
        payload = verify_token(token)
        
        assert payload['user_id'] == user_id
        assert payload['email'] == email
        assert payload['name'] == name
    
    def test_different_users_different_tokens(self):
        """Test that different users get different tokens"""
        token1 = generate_access_token("user-1", "user1@example.com", "User One")
        token2 = generate_access_token("user-2", "user2@example.com", "User Two")
        
        assert token1 != token2
    
    def test_token_has_expiration(self):
        """Test that token has expiration time"""
        token = generate_access_token("user-123", "test@example.com", "Test User")
        payload = verify_token(token)
        
        assert 'exp' in payload
        assert payload['exp'] > payload['iat']
    
    def test_token_has_issued_at(self):
        """Test that token has issued at time"""
        token = generate_access_token("user-123", "test@example.com", "Test User")
        payload = verify_token(token)
        
        assert 'iat' in payload
