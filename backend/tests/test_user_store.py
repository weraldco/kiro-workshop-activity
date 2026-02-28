"""
Tests for UserStore (MySQL version)
"""
import pytest
from app.store.user_store import UserStore
from app.database.connection import get_db_cursor


@pytest.fixture
def user_store():
    """Create a UserStore instance and clean up test data"""
    store = UserStore()
    
    yield store
    
    # Cleanup: Delete all test users after each test
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM users")


@pytest.fixture(autouse=True)
def cleanup_users():
    """Clean up users table before each test"""
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM users")


class TestUserStore:
    """Tests for UserStore"""
    
    def test_create_user_success(self, user_store):
        """Test creating a user successfully"""
        user = user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        assert user['email'] == "test@example.com"
        assert user['name'] == "Test User"
        assert 'id' in user
        assert 'created_at' in user
        assert 'updated_at' in user
        assert 'password_hash' not in user  # Should be sanitized
    
    def test_create_user_duplicate_email(self, user_store):
        """Test that creating user with duplicate email raises error"""
        user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        with pytest.raises(ValueError, match="already exists"):
            user_store.create_user(
                email="test@example.com",
                password_hash="another_hash",
                name="Another User"
            )
    
    def test_get_user_by_email_exists(self, user_store):
        """Test getting user by email when user exists"""
        created_user = user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        user = user_store.get_user_by_email("test@example.com")
        
        assert user is not None
        assert user['email'] == "test@example.com"
        assert user['name'] == "Test User"
        assert 'password_hash' in user  # Should include password_hash for auth
        assert user['password_hash'] == "hashed_password"
    
    def test_get_user_by_email_not_exists(self, user_store):
        """Test getting user by email when user doesn't exist"""
        user = user_store.get_user_by_email("nonexistent@example.com")
        
        assert user is None
    
    def test_get_user_by_id_exists(self, user_store):
        """Test getting user by ID when user exists"""
        created_user = user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        user = user_store.get_user_by_id(created_user['id'])
        
        assert user is not None
        assert user['id'] == created_user['id']
        assert user['email'] == "test@example.com"
        assert 'password_hash' not in user  # Should be sanitized
    
    def test_get_user_by_id_not_exists(self, user_store):
        """Test getting user by ID when user doesn't exist"""
        user = user_store.get_user_by_id("nonexistent-id")
        
        assert user is None
    
    def test_get_all_users(self, user_store):
        """Test getting all users"""
        user_store.create_user("user1@example.com", "hash1", "User One")
        user_store.create_user("user2@example.com", "hash2", "User Two")
        user_store.create_user("user3@example.com", "hash3", "User Three")
        
        users = user_store.get_all_users()
        
        assert len(users) == 3
        assert all('password_hash' not in u for u in users)  # All sanitized
        
        emails = [u['email'] for u in users]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "user3@example.com" in emails
    
    def test_get_all_users_empty(self, user_store):
        """Test getting all users when none exist"""
        users = user_store.get_all_users()
        
        assert users == []
    
    def test_update_user_name(self, user_store):
        """Test updating user name"""
        created_user = user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Old Name"
        )
        
        updated_user = user_store.update_user(
            created_user['id'],
            {"name": "New Name"}
        )
        
        assert updated_user is not None
        assert updated_user['name'] == "New Name"
        assert updated_user['email'] == "test@example.com"
    
    def test_update_user_email(self, user_store):
        """Test updating user email"""
        created_user = user_store.create_user(
            email="old@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        updated_user = user_store.update_user(
            created_user['id'],
            {"email": "new@example.com"}
        )
        
        assert updated_user is not None
        assert updated_user['email'] == "new@example.com"
    
    def test_update_user_email_duplicate(self, user_store):
        """Test that updating to duplicate email raises error"""
        user1 = user_store.create_user("user1@example.com", "hash1", "User One")
        user2 = user_store.create_user("user2@example.com", "hash2", "User Two")
        
        with pytest.raises(ValueError, match="already in use"):
            user_store.update_user(user2['id'], {"email": "user1@example.com"})
    
    def test_update_user_password_hash(self, user_store):
        """Test updating user password hash"""
        created_user = user_store.create_user(
            email="test@example.com",
            password_hash="old_hash",
            name="Test User"
        )
        
        updated_user = user_store.update_user(
            created_user['id'],
            {"password_hash": "new_hash"}
        )
        
        assert updated_user is not None
        
        # Verify password_hash was updated (check with get_user_by_email)
        user_with_hash = user_store.get_user_by_email("test@example.com")
        assert user_with_hash['password_hash'] == "new_hash"
    
    def test_update_user_not_exists(self, user_store):
        """Test updating user that doesn't exist"""
        updated_user = user_store.update_user(
            "nonexistent-id",
            {"name": "New Name"}
        )
        
        assert updated_user is None
    
    def test_delete_user_success(self, user_store):
        """Test deleting user successfully"""
        created_user = user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        result = user_store.delete_user(created_user['id'])
        
        assert result is True
        
        # Verify user is deleted
        user = user_store.get_user_by_id(created_user['id'])
        assert user is None
    
    def test_delete_user_not_exists(self, user_store):
        """Test deleting user that doesn't exist"""
        result = user_store.delete_user("nonexistent-id")
        
        assert result is False
    
    def test_sanitize_user_removes_password_hash(self, user_store):
        """Test that sanitize_user removes password_hash"""
        created_user = user_store.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        
        # Created user should not have password_hash
        assert 'password_hash' not in created_user
        
        # get_user_by_id should not have password_hash
        user = user_store.get_user_by_id(created_user['id'])
        assert 'password_hash' not in user
        
        # get_user_by_email SHOULD have password_hash (for auth)
        user_with_hash = user_store.get_user_by_email("test@example.com")
        assert 'password_hash' in user_with_hash
