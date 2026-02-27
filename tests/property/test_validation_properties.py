"""
Property-based tests for validation functions.

Tests verify that validation functions correctly accept valid inputs
and reject invalid inputs across a wide range of generated test cases.
"""

import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

from app.validators import (
    validate_status,
    validate_signup_enabled,
    validate_html_content
)


# Strategies for generating test data
valid_statuses = st.sampled_from(['pending', 'ongoing', 'completed'])
invalid_status_strings = st.text().filter(lambda s: s not in ['pending', 'ongoing', 'completed'])
invalid_status_types = st.one_of(
    st.integers(),
    st.booleans(),
    st.none(),
    st.lists(st.text()),
    st.floats(allow_nan=False)
)

valid_signup_enabled = st.booleans()
invalid_signup_enabled_types = st.one_of(
    st.text(),
    st.integers(),
    st.none(),
    st.lists(st.booleans()),
    st.floats(allow_nan=False)
)

valid_html_content = st.text(max_size=50 * 1024)  # Up to 50KB
invalid_html_content_types = st.one_of(
    st.integers(),
    st.booleans(),
    st.none(),
    st.lists(st.text()),
    st.floats(allow_nan=False)
)


@settings(max_examples=100)
@given(status=valid_statuses)
def test_property_2_status_value_validation_valid(status):
    """
    **Validates: Requirements 1.2, 2.2, 2.4**
    
    Feature: workshop-status-management-and-frontend, Property 2: Status Value Validation
    For any workshop creation or status update request with a valid status value 
    ("pending", "ongoing", or "completed"), the validation should succeed.
    """
    is_valid, error = validate_status(status)
    
    assert is_valid is True, f"Valid status '{status}' should be accepted"
    assert error == "", f"Valid status should have no error message, got: {error}"


@settings(max_examples=100)
@given(status=invalid_status_strings)
def test_property_2_status_value_validation_invalid_string(status):
    """
    **Validates: Requirements 1.2, 2.2, 2.4**
    
    Feature: workshop-status-management-and-frontend, Property 2: Status Value Validation
    For any workshop creation or status update request with a status value that is not 
    one of "pending", "ongoing", or "completed", the API should return a 400 status 
    with a descriptive error message.
    """
    is_valid, error = validate_status(status)
    
    assert is_valid is False, f"Invalid status string '{status}' should be rejected"
    assert error != "", "Invalid status should have an error message"
    assert "pending" in error and "ongoing" in error and "completed" in error, \
        f"Error message should list valid statuses, got: {error}"


@settings(max_examples=100)
@given(status=invalid_status_types)
def test_property_2_status_value_validation_invalid_type(status):
    """
    **Validates: Requirements 1.2, 2.2, 2.4**
    
    Feature: workshop-status-management-and-frontend, Property 2: Status Value Validation
    For any workshop creation or status update request with a status value that is not 
    a string, the validation should fail with a descriptive error message.
    """
    is_valid, error = validate_status(status)
    
    assert is_valid is False, f"Non-string status {type(status).__name__} should be rejected"
    assert error != "", "Invalid status type should have an error message"
    assert "pending" in error and "ongoing" in error and "completed" in error, \
        f"Error message should list valid statuses, got: {error}"


@settings(max_examples=100)
@given(signup_enabled=valid_signup_enabled)
def test_property_10_signup_enabled_validation_valid(signup_enabled):
    """
    **Validates: Requirements 4.4**
    
    Feature: workshop-status-management-and-frontend, Property 10: Signup Enabled Validation
    For any signup enabled update request with a boolean value (true or false),
    the validation should succeed.
    """
    is_valid, error = validate_signup_enabled(signup_enabled)
    
    assert is_valid is True, f"Valid boolean value {signup_enabled} should be accepted"
    assert error == "", f"Valid signup_enabled should have no error message, got: {error}"


@settings(max_examples=100)
@given(signup_enabled=invalid_signup_enabled_types)
def test_property_10_signup_enabled_validation_invalid(signup_enabled):
    """
    **Validates: Requirements 4.4**
    
    Feature: workshop-status-management-and-frontend, Property 10: Signup Enabled Validation
    For any signup enabled update request with a non-boolean value, the API should 
    return a 400 status with a descriptive error message.
    """
    is_valid, error = validate_signup_enabled(signup_enabled)
    
    assert is_valid is False, f"Non-boolean value {type(signup_enabled).__name__} should be rejected"
    assert error != "", "Invalid signup_enabled should have an error message"
    assert "boolean" in error.lower(), f"Error message should mention 'boolean', got: {error}"


@settings(max_examples=100)
@given(html_content=valid_html_content)
def test_property_17_html_content_type_validation_valid(html_content):
    """
    **Validates: Requirements 7.2, 8.3**
    
    Feature: workshop-status-management-and-frontend, Property 17: HTML Content Type Validation
    For any challenge creation request with html_content that is a string type 
    (including empty string), the validation should succeed.
    """
    is_valid, error = validate_html_content(html_content)
    
    assert is_valid is True, f"Valid string html_content should be accepted"
    assert error == "", f"Valid html_content should have no error message, got: {error}"


@settings(max_examples=100)
@given(html_content=st.text(min_size=1))
def test_property_17_html_content_empty_string_valid(html_content):
    """
    **Validates: Requirements 7.2, 8.3**
    
    Feature: workshop-status-management-and-frontend, Property 17: HTML Content Type Validation
    Empty string should be accepted as valid html_content.
    """
    # Test with empty string explicitly
    is_valid, error = validate_html_content("")
    
    assert is_valid is True, "Empty string should be accepted as valid html_content"
    assert error == "", f"Empty string should have no error message, got: {error}"


@settings(max_examples=100)
@given(html_content=invalid_html_content_types)
def test_property_17_html_content_type_validation_invalid(html_content):
    """
    **Validates: Requirements 7.2, 8.3**
    
    Feature: workshop-status-management-and-frontend, Property 17: HTML Content Type Validation
    For any challenge creation request with html_content that is not a string type,
    the API should return a 400 status with a descriptive error message.
    """
    is_valid, error = validate_html_content(html_content)
    
    assert is_valid is False, f"Non-string html_content {type(html_content).__name__} should be rejected"
    assert error != "", "Invalid html_content type should have an error message"
    assert "string" in error.lower(), f"Error message should mention 'string', got: {error}"


@settings(max_examples=20)  # Fewer examples since we're generating large strings
@given(extra_bytes=st.integers(min_value=1, max_value=1000))
def test_property_17_html_content_max_length_validation(extra_bytes):
    """
    **Validates: Requirements 7.2, 8.3**
    
    Feature: workshop-status-management-and-frontend, Property 17: HTML Content Type Validation
    For any challenge creation request with html_content exceeding 50KB,
    the validation should fail with a descriptive error message (DoS prevention).
    """
    # Create content exceeding 50KB
    max_length = 50 * 1024
    large_content = "a" * (max_length + extra_bytes)
    
    is_valid, error = validate_html_content(large_content)
    
    assert is_valid is False, f"html_content exceeding 50KB should be rejected"
    assert error != "", "Oversized html_content should have an error message"
    assert "50" in error or "KB" in error.upper(), \
        f"Error message should mention size limit, got: {error}"
