# Implementation Plan: Workshop Management Backend

## Overview

This plan implements a Flask-based REST API for workshop management with JSON file persistence. The implementation follows a three-layer architecture (API routes, business logic, data access) and includes comprehensive validation, error handling, and testing.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create directory structure: `app/`, `app/routes/`, `app/services/`, `app/store/`, `tests/unit/`, `tests/property/`, `tests/integration/`
  - Create `requirements.txt` with Flask, pytest, hypothesis dependencies
  - Create `app/__init__.py` to initialize Flask application
  - Set up JSON file path configuration
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 2. Implement data access layer
  - [x] 2.1 Create file locking mechanism
    - Implement `app/store/file_lock.py` with `FileLock` context manager
    - Support exclusive file locking for thread-safe writes
    - _Requirements: 9.5_
  
  - [x] 2.2 Implement workshop store
    - Create `app/store/workshop_store.py` with `WorkshopStore` class
    - Implement `load_data()`, `save_data()`, `add_workshop()`, `get_workshop()`, `get_all_workshops()`
    - Implement `add_challenge()`, `get_challenges()`, `add_registration()`, `get_all_registrations()`, `get_registrations_for_workshop()`, `update_workshop()`
    - Initialize JSON file with empty structure if it doesn't exist
    - Use file locking for all write operations
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [x] 2.3 Write property test for persistence round-trip
    - **Property 6: Persistence Round-Trip**
    - **Validates: Requirements 1.8, 4.6, 6.6, 9.1, 9.2, 9.3, 9.4**

- [-] 3. Implement validation layer
  - [x] 3.1 Create input validators
    - Create `app/validators.py` with validation functions
    - Implement `validate_workshop_data()` for title, time range, capacity, delivery mode
    - Implement `validate_challenge_data()` for title validation
    - Implement `validate_registration_data()` for required fields
    - Implement `validate_delivery_mode()` and `validate_time_range()` helpers
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 4.3, 8.2, 8.3_
  
  - [ ]* 3.2 Write property tests for validation
    - **Property 2: Non-Empty Title Validation**
    - **Validates: Requirements 1.2, 4.3**
  
  - [ ]* 3.3 Write property test for time range validation
    - **Property 3: Time Range Validation**
    - **Validates: Requirements 1.3**
  
  - [ ]* 3.4 Write property test for capacity validation
    - **Property 4: Positive Capacity Validation**
    - **Validates: Requirements 1.4**
  
  - [ ]* 3.5 Write property test for delivery mode validation
    - **Property 5: Delivery Mode Validation**
    - **Validates: Requirements 1.5**

- [x] 4. Implement business logic layer
  - [x] 4.1 Create workshop service
    - Create `app/services/workshop_service.py` with `WorkshopService` class
    - Implement `create_workshop()` with UUID generation and registration count initialization
    - Implement `get_workshop()`, `list_workshops()`, `workshop_exists()`
    - Generate ISO 8601 timestamps for workshop times
    - _Requirements: 1.1, 1.7, 2.1, 3.1, 10.4_
  
  - [x] 4.2 Create challenge service
    - Create `app/services/challenge_service.py` with `ChallengeService` class
    - Implement `create_challenge()` with UUID generation and timestamp
    - Implement `list_challenges()` for workshop-specific challenges
    - _Requirements: 4.1, 5.1_
  
  - [x] 4.3 Create registration service
    - Create `app/services/registration_service.py` with `RegistrationService` class
    - Implement `register_participant()` with capacity checking and count increment
    - Implement `list_registrations()`, `get_registration_count()`
    - Generate ISO 8601 timestamps for registrations
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 7.1, 10.4_
  
  - [ ]* 4.4 Write property test for registration count invariant
    - **Property 13: Registration Count Invariant**
    - **Validates: Requirements 6.4**

- [x] 5. Checkpoint - Ensure core logic tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement API layer
  - [x] 6.1 Create Flask application entry point
    - Create `app.py` with Flask app initialization
    - Configure JSON file path
    - Register error handlers for 400, 404, 409, 500
    - Set up CORS if needed
    - _Requirements: 11.1, 11.2_
  
  - [x] 6.2 Implement workshop routes
    - Create `app/routes/workshop_routes.py` with Flask blueprint
    - Implement `POST /api/workshop` endpoint with validation and 201 response
    - Implement `GET /api/workshop` endpoint with 200 response
    - Implement `GET /api/workshop/<workshop_id>` endpoint with 200/404 responses
    - Use standardized response format: `{"success": true/false, "data": {}, "error": "..."}`
    - Set Content-Type header to application/json
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 10.1, 10.2, 10.3_
  
  - [x] 6.3 Implement challenge routes
    - Add `POST /api/workshop/<workshop_id>/challenge` endpoint to workshop routes
    - Validate workshop existence, return 404 if not found
    - Validate challenge data, return 400 if invalid
    - Return 201 with challenge ID on success
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [x] 6.4 Implement registration routes
    - Add `POST /api/workshop/<workshop_id>/register` endpoint to workshop routes
    - Validate workshop existence, return 404 if not found
    - Check capacity, return 409 if full
    - Return 201 with registration ID on success
    - Add `GET /api/workshop/registrations` endpoint
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3_
  
  - [ ]* 6.5 Write property test for workshop creation
    - **Property 1: Workshop Creation with Valid Data**
    - **Validates: Requirements 1.1, 1.7, 2.1**
  
  - [ ]* 6.6 Write property test for non-existent resource handling
    - **Property 7: Non-Existent Resource Returns 404**
    - **Validates: Requirements 2.2, 4.2, 6.5**
  
  - [ ]* 6.7 Write property test for complete workshop data
    - **Property 8: Complete Workshop Data in Responses**
    - **Validates: Requirements 2.3, 3.3**
  
  - [ ]* 6.8 Write property test for listing workshops
    - **Property 9: List All Created Workshops**
    - **Validates: Requirements 3.1**
  
  - [ ]* 6.9 Write property test for challenge creation
    - **Property 10: Challenge Creation for Existing Workshop**
    - **Validates: Requirements 4.1, 5.1**
  
  - [ ]* 6.10 Write property test for registration creation
    - **Property 11: Registration Creation and Count Increment**
    - **Validates: Requirements 6.1, 6.2**
  
  - [ ]* 6.11 Write property test for capacity enforcement
    - **Property 12: Capacity Enforcement**
    - **Validates: Requirements 6.3**
  
  - [ ]* 6.12 Write property test for listing registrations
    - **Property 14: List All Created Registrations**
    - **Validates: Requirements 7.1**
  
  - [ ]* 6.13 Write property test for complete registration data
    - **Property 15: Complete Registration Data in Responses**
    - **Validates: Requirements 7.3**

- [x] 7. Implement error handling
  - [x] 7.1 Add request validation error handling
    - Handle malformed JSON with 400 response
    - Handle missing required fields with 400 response
    - Handle invalid data types with 400 response
    - Include descriptive error messages in all error responses
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [x] 7.2 Add global error handlers
    - Register Flask error handlers for 400, 404, 409, 500
    - Ensure all error responses use standardized format
    - _Requirements: 1.6, 2.2, 4.4, 4.5, 5.4, 5.5, 6.3, 6.5, 8.4_
  
  - [ ]* 7.3 Write property test for missing fields validation
    - **Property 16: Missing Required Fields Validation**
    - **Validates: Requirements 8.2**
  
  - [ ]* 7.4 Write property test for invalid data type validation
    - **Property 17: Invalid Data Type Validation**
    - **Validates: Requirements 8.3**

- [x] 8. Implement response formatting
  - [x] 8.1 Ensure consistent JSON response format
    - Verify all endpoints return `{"success": true/false, "data": {}, "error": "..."}`
    - Verify Content-Type header is application/json
    - Verify timestamps use ISO 8601 format
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  
  - [ ]* 8.2 Write property test for JSON response format
    - **Property 18: JSON Response Format**
    - **Validates: Requirements 10.1, 10.2**
  
  - [ ]* 8.3 Write property test for ISO 8601 timestamps
    - **Property 19: ISO 8601 Timestamp Format**
    - **Validates: Requirements 10.4**

- [x] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Write unit tests for specific scenarios
  - [x]* 10.1 Write unit tests for workshop routes
    - Test specific valid workshop creation example
    - Test empty workshop list scenario
    - Test specific workshop retrieval by ID
    - _Requirements: 1.1, 2.1, 3.2_
  
  - [x]* 10.2 Write unit tests for challenge routes
    - Test specific valid challenge creation example
    - Test challenge creation for non-existent workshop
    - _Requirements: 4.1, 4.4_
  
  - [x]* 10.3 Write unit tests for registration routes
    - Test specific valid registration example
    - Test registration for workshop at capacity
    - Test empty registration list scenario
    - _Requirements: 6.1, 6.3, 7.2_
  
  - [x]* 10.4 Write unit tests for validators
    - Test specific validation edge cases
    - Test malformed JSON handling
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [x]* 10.5 Write unit tests for file locking
    - Test concurrent write operations
    - Verify file lock prevents race conditions
    - _Requirements: 9.5_

- [x] 11. Create application entry point and documentation
  - [x] 11.1 Create main entry point
    - Create `run.py` or update `app.py` with `if __name__ == '__main__'` block
    - Configure Flask to run on appropriate host/port
    - _Requirements: 11.1, 11.2_
  
  - [x] 11.2 Create README with setup instructions
    - Document how to install dependencies
    - Document how to run the application
    - Document API endpoints and request/response formats
    - Include example curl commands for testing

- [x] 12. Final checkpoint - Verify complete implementation
  - Run all tests (unit, property, integration)
  - Verify JSON file persistence works across restarts
  - Test all API endpoints manually
  - Ensure all requirements are met
  - Ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties across 100+ random inputs
- Unit tests validate specific examples, edge cases, and integration points
- The implementation uses Python Flask with JSON file storage as specified
- All API responses follow the standardized format: `{"success": true/false, "data": {}, "error": "..."}`
- File locking ensures thread-safe concurrent access to the JSON data store
