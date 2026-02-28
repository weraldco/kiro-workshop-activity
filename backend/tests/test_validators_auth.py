"""
Tests for authentication validators
"""
import pytest
from app.validators import (
    validate_email,
    validate_password,
    validate_user_name,
    validate_user_registration,
    validate_user_login
)


class TestEmailValidation:
    """Tests for email validation"""
    
    def test_valid_email(self):
        """Test valid email addresses"""
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
            "123@example.com",
            "a@b.co"
        ]
        
        for email in valid_emails:
            is_valid, error = validate_email(email)
            assert is_valid is True, f"Email {email} should be valid"
            assert error == ""
    
    def test_invalid_email_format(self):
        """Test invalid email formats"""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com",
            "user@example",
            ""
        ]
        
        for email in invalid_emails:
            is_valid, error = validate_email(email)
            assert is_valid is False, f"Email {email} should be invalid"
            assert error != ""
    
    def test_email_too_long(self):
        """Test email that's too long"""
        long_email = "a" * 250 + "@example.com"
        is_valid, error = validate_email(long_email)
        
        assert is_valid is False
        assert "255 characters" in error
    
    def test_email_required(self):
        """Test that email is required"""
        is_valid, error = validate_email("")
        
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_email_must_be_string(self):
        """Test that email must be a string"""
        is_valid, error = validate_email(123)
        
        assert is_valid is False
        assert "string" in error.lower()


class TestPasswordValidation:
    """Tests for password validation"""
    
    def test_valid_password(self):
        """Test valid passwords"""
        valid_passwords = [
            "Password123!",
            "MyP@ssw0rd",
            "Str0ng!Pass",
            "C0mpl3x#Pwd",
            "Test123!@#"
        ]
        
        for password in valid_passwords:
            is_valid, error = validate_password(password)
            assert is_valid is True, f"Password {password} should be valid"
            assert error == ""
    
    def test_password_too_short(self):
        """Test password that's too short"""
        is_valid, error = validate_password("Pass1!")
        
        assert is_valid is False
        assert "8 characters" in error
    
    def test_password_too_long(self):
        """Test password that's too long"""
        long_password = "A" * 130 + "a1!"
        is_valid, error = validate_password(long_password)
        
        assert is_valid is False
        assert "128 characters" in error
    
    def test_password_no_uppercase(self):
        """Test password without uppercase letter"""
        is_valid, error = validate_password("password123!")
        
        assert is_valid is False
        assert "uppercase" in error.lower()
    
    def test_password_no_lowercase(self):
        """Test password without lowercase letter"""
        is_valid, error = validate_password("PASSWORD123!")
        
        assert is_valid is False
        assert "lowercase" in error.lower()
    
    def test_password_no_number(self):
        """Test password without number"""
        is_valid, error = validate_password("Password!")
        
        assert is_valid is False
        assert "number" in error.lower()
    
    def test_password_no_special_char(self):
        """Test password without special character"""
        is_valid, error = validate_password("Password123")
        
        assert is_valid is False
        assert "special character" in error.lower()
    
    def test_password_required(self):
        """Test that password is required"""
        is_valid, error = validate_password("")
        
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_password_must_be_string(self):
        """Test that password must be a string"""
        is_valid, error = validate_password(12345678)
        
        assert is_valid is False
        assert "string" in error.lower()


class TestUserNameValidation:
    """Tests for user name validation"""
    
    def test_valid_name(self):
        """Test valid names"""
        valid_names = [
            "John Doe",
            "Jane",
            "Mary-Jane Smith",
            "José García",
            "李明",
            "A"
        ]
        
        for name in valid_names:
            is_valid, error = validate_user_name(name)
            assert is_valid is True, f"Name '{name}' should be valid"
            assert error == ""
    
    def test_name_too_long(self):
        """Test name that's too long"""
        long_name = "A" * 101
        is_valid, error = validate_user_name(long_name)
        
        assert is_valid is False
        assert "100 characters" in error
    
    def test_name_empty(self):
        """Test empty name"""
        is_valid, error = validate_user_name("")
        
        assert is_valid is False
        assert "required" in error.lower() or "empty" in error.lower()
    
    def test_name_whitespace_only(self):
        """Test name with only whitespace"""
        is_valid, error = validate_user_name("   ")
        
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_name_must_be_string(self):
        """Test that name must be a string"""
        is_valid, error = validate_user_name(123)
        
        assert is_valid is False
        assert "string" in error.lower()


class TestUserRegistrationValidation:
    """Tests for user registration validation"""
    
    def test_valid_registration(self):
        """Test valid registration data"""
        is_valid, error = validate_user_registration(
            email="test@example.com",
            password="Password123!",
            name="Test User"
        )
        
        assert is_valid is True
        assert error == ""
    
    def test_invalid_email(self):
        """Test registration with invalid email"""
        is_valid, error = validate_user_registration(
            email="invalid-email",
            password="Password123!",
            name="Test User"
        )
        
        assert is_valid is False
        assert "email" in error.lower()
    
    def test_invalid_password(self):
        """Test registration with invalid password"""
        is_valid, error = validate_user_registration(
            email="test@example.com",
            password="weak",
            name="Test User"
        )
        
        assert is_valid is False
        assert "password" in error.lower()
    
    def test_invalid_name(self):
        """Test registration with invalid name"""
        is_valid, error = validate_user_registration(
            email="test@example.com",
            password="Password123!",
            name=""
        )
        
        assert is_valid is False
        assert "name" in error.lower()


class TestUserLoginValidation:
    """Tests for user login validation"""
    
    def test_valid_login(self):
        """Test valid login data"""
        is_valid, error = validate_user_login(
            email="test@example.com",
            password="any-password"
        )
        
        assert is_valid is True
        assert error == ""
    
    def test_missing_email(self):
        """Test login with missing email"""
        is_valid, error = validate_user_login(
            email="",
            password="password"
        )
        
        assert is_valid is False
        assert "email" in error.lower()
    
    def test_missing_password(self):
        """Test login with missing password"""
        is_valid, error = validate_user_login(
            email="test@example.com",
            password=""
        )
        
        assert is_valid is False
        assert "password" in error.lower()
