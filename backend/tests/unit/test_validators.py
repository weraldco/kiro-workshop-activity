"""
Unit tests for input validators.
"""

import pytest
from datetime import datetime
from app.validators import (
    validate_delivery_mode,
    validate_time_range,
    validate_workshop_data,
    validate_challenge_data,
    validate_registration_data,
    validate_status,
    validate_signup_enabled,
    validate_html_content,
    validate_email_format
)


class TestDeliveryModeValidation:
    """Tests for delivery mode validation."""
    
    def test_valid_delivery_modes(self):
        """Test that valid delivery modes are accepted."""
        assert validate_delivery_mode("online") is True
        assert validate_delivery_mode("face-to-face") is True
        assert validate_delivery_mode("hybrid") is True
    
    def test_invalid_delivery_mode_string(self):
        """Test that invalid delivery mode strings are rejected."""
        assert validate_delivery_mode("in-person") is False
        assert validate_delivery_mode("remote") is False
        assert validate_delivery_mode("") is False
    
    def test_invalid_delivery_mode_type(self):
        """Test that non-string delivery modes are rejected."""
        assert validate_delivery_mode(123) is False
        assert validate_delivery_mode(None) is False
        assert validate_delivery_mode(["online"]) is False


class TestTimeRangeValidation:
    """Tests for time range validation."""
    
    def test_valid_time_range_strings(self):
        """Test that valid time ranges (start < end) are accepted."""
        assert validate_time_range("2024-01-01T10:00:00", "2024-01-01T12:00:00") is True
        assert validate_time_range("2024-01-01T10:00:00Z", "2024-01-02T10:00:00Z") is True
    
    def test_valid_time_range_datetime(self):
        """Test that valid datetime objects are accepted."""
        start = datetime(2024, 1, 1, 10, 0)
        end = datetime(2024, 1, 1, 12, 0)
        assert validate_time_range(start, end) is True
    
    def test_invalid_time_range_end_before_start(self):
        """Test that time ranges where end <= start are rejected."""
        assert validate_time_range("2024-01-01T12:00:00", "2024-01-01T10:00:00") is False
        assert validate_time_range("2024-01-01T10:00:00", "2024-01-01T10:00:00") is False
    
    def test_invalid_time_format(self):
        """Test that invalid time formats are rejected."""
        assert validate_time_range("invalid", "2024-01-01T10:00:00") is False
        assert validate_time_range("2024-01-01T10:00:00", "invalid") is False
    
    def test_invalid_time_type(self):
        """Test that invalid time types are rejected."""
        assert validate_time_range(123, "2024-01-01T10:00:00") is False
        assert validate_time_range("2024-01-01T10:00:00", None) is False


class TestWorkshopDataValidation:
    """Tests for workshop data validation."""
    
    def test_valid_workshop_data(self):
        """Test that valid workshop data is accepted."""
        data = {
            'title': 'Python Workshop',
            'description': 'Learn Python',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is True
        assert error == ""
    
    def test_missing_required_fields(self):
        """Test that missing required fields are detected."""
        data = {'title': 'Workshop'}
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "Missing required fields" in error
    
    def test_empty_title(self):
        """Test that empty title is rejected."""
        data = {
            'title': '',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "non-empty" in error.lower()
    
    def test_whitespace_only_title(self):
        """Test that whitespace-only title is rejected."""
        data = {
            'title': '   ',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "non-empty" in error.lower()
    
    def test_invalid_capacity_zero(self):
        """Test that zero capacity is rejected."""
        data = {
            'title': 'Workshop',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': 0,
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "positive" in error.lower()
    
    def test_invalid_capacity_negative(self):
        """Test that negative capacity is rejected."""
        data = {
            'title': 'Workshop',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': -5,
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "positive" in error.lower()
    
    def test_invalid_capacity_type(self):
        """Test that non-integer capacity is rejected."""
        data = {
            'title': 'Workshop',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': "20",
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "integer" in error.lower()
    
    def test_invalid_delivery_mode(self):
        """Test that invalid delivery mode is rejected."""
        data = {
            'title': 'Workshop',
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'in-person'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "delivery mode" in error.lower()
    
    def test_invalid_time_range(self):
        """Test that invalid time range is rejected."""
        data = {
            'title': 'Workshop',
            'start_time': '2024-01-01T12:00:00',
            'end_time': '2024-01-01T10:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        is_valid, error = validate_workshop_data(data)
        assert is_valid is False
        assert "before" in error.lower()


class TestChallengeDataValidation:
    """Tests for challenge data validation."""
    
    def test_valid_challenge_data(self):
        """Test that valid challenge data is accepted."""
        data = {
            'title': 'Build a REST API',
            'description': 'Create a simple REST API',
            'html_content': '<p>Challenge content</p>'
        }
        is_valid, error = validate_challenge_data(data)
        assert is_valid is True
        assert error == ""
    
    def test_missing_title(self):
        """Test that missing title is detected."""
        data = {
            'description': 'Some description',
            'html_content': '<p>Content</p>'
        }
        is_valid, error = validate_challenge_data(data)
        assert is_valid is False
        assert "title" in error.lower()
    
    def test_empty_title(self):
        """Test that empty title is rejected."""
        data = {
            'title': '',
            'description': 'Some description',
            'html_content': '<p>Content</p>'
        }
        is_valid, error = validate_challenge_data(data)
        assert is_valid is False
        assert "non-empty" in error.lower()
    
    def test_whitespace_only_title(self):
        """Test that whitespace-only title is rejected."""
        data = {
            'title': '   ',
            'description': 'Some description',
            'html_content': '<p>Content</p>'
        }
        is_valid, error = validate_challenge_data(data)
        assert is_valid is False
        assert "non-empty" in error.lower()
    
    def test_invalid_title_type(self):
        """Test that non-string title is rejected."""
        data = {
            'title': 123,
            'description': 'Some description',
            'html_content': '<p>Content</p>'
        }
        is_valid, error = validate_challenge_data(data)
        assert is_valid is False
        assert "string" in error.lower()


class TestRegistrationDataValidation:
    """Tests for registration data validation."""
    
    def test_valid_registration_data(self):
        """Test that valid registration data is accepted."""
        data = {
            'participant_name': 'John Doe',
            'participant_email': 'john@example.com'
        }
        is_valid, error = validate_registration_data(data)
        assert is_valid is True
        assert error == ""
    
    def test_missing_participant_name(self):
        """Test that missing participant_name is detected."""
        data = {'participant_email': 'john@example.com'}
        is_valid, error = validate_registration_data(data)
        assert is_valid is False
        assert "participant_name" in error.lower()
    
    def test_missing_participant_email(self):
        """Test that missing participant_email is detected."""
        data = {'participant_name': 'John Doe'}
        is_valid, error = validate_registration_data(data)
        assert is_valid is False
        assert "participant_email" in error.lower()
    
    def test_missing_both_fields(self):
        """Test that missing both fields is detected."""
        data = {}
        is_valid, error = validate_registration_data(data)
        assert is_valid is False
        assert "missing required fields" in error.lower()



class TestStatusValidation:
    """Tests for status validation."""
    
    def test_valid_status_values(self):
        """Test that valid status values are accepted."""
        is_valid, error = validate_status("pending")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validate_status("ongoing")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validate_status("completed")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_status_string(self):
        """Test that invalid status strings are rejected."""
        is_valid, error = validate_status("active")
        assert is_valid is False
        assert "pending, ongoing, completed" in error
        
        is_valid, error = validate_status("finished")
        assert is_valid is False
        assert "pending, ongoing, completed" in error
        
        is_valid, error = validate_status("")
        assert is_valid is False
        assert "pending, ongoing, completed" in error
    
    def test_invalid_status_type(self):
        """Test that non-string status values are rejected."""
        is_valid, error = validate_status(123)
        assert is_valid is False
        assert "pending, ongoing, completed" in error
        
        is_valid, error = validate_status(None)
        assert is_valid is False
        assert "pending, ongoing, completed" in error
        
        is_valid, error = validate_status(["pending"])
        assert is_valid is False
        assert "pending, ongoing, completed" in error


class TestSignupEnabledValidation:
    """Tests for signup_enabled validation."""
    
    def test_valid_signup_enabled_values(self):
        """Test that boolean values are accepted."""
        is_valid, error = validate_signup_enabled(True)
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validate_signup_enabled(False)
        assert is_valid is True
        assert error == ""
    
    def test_invalid_signup_enabled_type(self):
        """Test that non-boolean values are rejected."""
        is_valid, error = validate_signup_enabled("true")
        assert is_valid is False
        assert "boolean" in error.lower()
        
        is_valid, error = validate_signup_enabled(1)
        assert is_valid is False
        assert "boolean" in error.lower()
        
        is_valid, error = validate_signup_enabled(0)
        assert is_valid is False
        assert "boolean" in error.lower()
        
        is_valid, error = validate_signup_enabled(None)
        assert is_valid is False
        assert "boolean" in error.lower()


class TestHtmlContentValidation:
    """Tests for html_content validation."""
    
    def test_valid_html_content_string(self):
        """Test that string values are accepted."""
        is_valid, error = validate_html_content("<p>Hello</p>")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validate_html_content("<div><h1>Title</h1><p>Content</p></div>")
        assert is_valid is True
        assert error == ""
    
    def test_valid_empty_html_content(self):
        """Test that empty string is accepted."""
        is_valid, error = validate_html_content("")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_html_content_type(self):
        """Test that non-string values are rejected."""
        is_valid, error = validate_html_content(123)
        assert is_valid is False
        assert "string" in error.lower()
        
        is_valid, error = validate_html_content(None)
        assert is_valid is False
        assert "string" in error.lower()
        
        is_valid, error = validate_html_content(["<p>Hello</p>"])
        assert is_valid is False
        assert "string" in error.lower()
    
    def test_html_content_max_length(self):
        """Test that content exceeding 50KB is rejected."""
        # Create content just under 50KB
        small_content = "a" * (50 * 1024 - 1)
        is_valid, error = validate_html_content(small_content)
        assert is_valid is True
        assert error == ""
        
        # Create content exceeding 50KB
        large_content = "a" * (50 * 1024 + 1)
        is_valid, error = validate_html_content(large_content)
        assert is_valid is False
        assert "50KB" in error or "50" in error


class TestEmailFormatValidation:
    """Tests for email format validation."""
    
    def test_valid_email_formats(self):
        """Test that valid email formats are accepted."""
        is_valid, error = validate_email_format("user@example.com")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validate_email_format("john.doe@company.co.uk")
        assert is_valid is True
        assert error == ""
        
        is_valid, error = validate_email_format("test+tag@domain.org")
        assert is_valid is True
        assert error == ""
    
    def test_invalid_email_formats(self):
        """Test that invalid email formats are rejected."""
        is_valid, error = validate_email_format("invalid")
        assert is_valid is False
        assert "email" in error.lower()
        
        is_valid, error = validate_email_format("@example.com")
        assert is_valid is False
        assert "email" in error.lower()
        
        is_valid, error = validate_email_format("user@")
        assert is_valid is False
        assert "email" in error.lower()
        
        is_valid, error = validate_email_format("user@domain")
        assert is_valid is False
        assert "email" in error.lower()
        
        is_valid, error = validate_email_format("")
        assert is_valid is False
        assert "email" in error.lower()
    
    def test_invalid_email_type(self):
        """Test that non-string email values are rejected."""
        is_valid, error = validate_email_format(123)
        assert is_valid is False
        assert "string" in error.lower()
        
        is_valid, error = validate_email_format(None)
        assert is_valid is False
        assert "string" in error.lower()
