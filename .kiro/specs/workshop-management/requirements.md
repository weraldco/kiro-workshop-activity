# Requirements Document

## Introduction

This document defines the requirements for a workshop management backend system. The system provides a REST API starting at `/api/workshop` for organizers to create and manage workshops, and for participants to register for workshops. The backend is implemented using Python and Flask, with data persisted to a JSON file in the project directory.

## Glossary

- **Workshop_API**: The Flask-based REST API that handles workshop management operations at `/api/workshop`
- **Workshop**: An event entity with properties including title, description, start time, end time, capacity, delivery mode, and current registration count
- **Challenge**: A task or activity associated with a workshop that participants complete
- **Organizer**: A user who creates and manages workshop events
- **Participant**: A user who registers for and attends workshops
- **Registration**: A record of a participant's enrollment in a workshop
- **Workshop_Store**: The JSON file-based persistence layer that stores workshop data in the project directory
- **Workshop_ID**: A unique identifier assigned to each workshop
- **Challenge_ID**: A unique identifier assigned to each challenge
- **Registration_ID**: A unique identifier assigned to each registration
- **Delivery_Mode**: The format of workshop delivery, with values: "online", "face-to-face", or "hybrid"

## Requirements

### Requirement 1: Create Workshop

**User Story:** As an Organizer, I want to create a new workshop with details, so that participants can discover and register for it

#### Acceptance Criteria

1. WHEN an Organizer sends a POST request to `/api/workshop` with valid workshop data, THE Workshop_API SHALL create a new Workshop and return a 201 status with the Workshop_ID
2. THE Workshop_API SHALL validate that title is a non-empty string
3. THE Workshop_API SHALL validate that start_time occurs before end_time
4. THE Workshop_API SHALL validate that capacity is a positive integer
5. THE Workshop_API SHALL validate that delivery_mode is one of: "online", "face-to-face", or "hybrid"
6. IF the request contains invalid data, THEN THE Workshop_API SHALL return a 400 status with a descriptive error message
7. THE Workshop_API SHALL initialize the registration count to zero for new workshops
8. THE Workshop_Store SHALL persist the new Workshop to the JSON file in the project directory

### Requirement 2: Retrieve Specific Workshop

**User Story:** As an Organizer, I want to view a specific workshop's details, so that I can review its configuration and status

#### Acceptance Criteria

1. WHEN an Organizer requests a Workshop by Workshop_ID from `/api/workshop/{id}`, THE Workshop_API SHALL return the complete workshop data with a 200 status
2. IF the Workshop_ID does not exist, THEN THE Workshop_API SHALL return a 404 status
3. THE Workshop_API SHALL include all workshop properties in the response: title, description, start_time, end_time, capacity, delivery_mode, and current registration count

### Requirement 3: List All Workshops

**User Story:** As an Organizer, I want to retrieve all workshops I have created, so that I can manage them effectively

#### Acceptance Criteria

1. WHEN an Organizer requests the workshop list from `/api/workshop`, THE Workshop_API SHALL return all workshops with a 200 status
2. THE Workshop_API SHALL return an empty list when no workshops exist
3. THE Workshop_API SHALL include all workshop properties for each workshop in the list: title, description, start_time, end_time, capacity, delivery_mode, and current registration count

### Requirement 4: Create Challenge for Workshop

**User Story:** As an Organizer, I want to create challenges for each workshop, so that participants have structured activities to complete

#### Acceptance Criteria

1. WHEN an Organizer sends a POST request to `/api/workshop/{id}/challenge` with valid challenge data, THE Workshop_API SHALL create a new Challenge and return a 201 status with the Challenge_ID
2. THE Workshop_API SHALL validate that the Workshop_ID exists
3. THE Workshop_API SHALL validate that challenge title is a non-empty string
4. IF the Workshop_ID does not exist, THEN THE Workshop_API SHALL return a 404 status
5. IF the request contains invalid data, THEN THE Workshop_API SHALL return a 400 status with a descriptive error message
6. THE Workshop_Store SHALL persist the new Challenge to the JSON file in the project directory

### Requirement 5: Participant Challenge Creation

**User Story:** As a Participant, I want to create one challenge for a workshop, so that I can contribute to the workshop content

#### Acceptance Criteria

1. WHEN a Participant sends a POST request to `/api/workshop/{id}/challenge` with valid challenge data, THE Workshop_API SHALL create a new Challenge and return a 201 status with the Challenge_ID
2. THE Workshop_API SHALL validate that the Workshop_ID exists
3. THE Workshop_API SHALL validate that challenge title is a non-empty string
4. IF the Workshop_ID does not exist, THEN THE Workshop_API SHALL return a 404 status
5. IF the request contains invalid data, THEN THE Workshop_API SHALL return a 400 status with a descriptive error message
6. THE Workshop_Store SHALL persist the new Challenge to the JSON file in the project directory

### Requirement 6: Register for Workshop

**User Story:** As a Participant, I want to register for a workshop, so that I can secure my spot and participate

#### Acceptance Criteria

1. WHEN a Participant sends a POST request to `/api/workshop/{id}/register` with valid registration data, THE Workshop_API SHALL create a Registration and return a 201 status with the Registration_ID
2. THE Workshop_API SHALL increment the workshop registration count
3. IF the registration count equals capacity, THEN THE Workshop_API SHALL return a 409 status indicating the workshop is full
4. THE Workshop_API SHALL ensure the registration count does not exceed capacity
5. IF the Workshop_ID does not exist, THEN THE Workshop_API SHALL return a 404 status
6. THE Workshop_Store SHALL persist the new Registration to the JSON file in the project directory

### Requirement 7: View All Registrations

**User Story:** As an Organizer, I want to see all registrations for workshops, so that I can track attendance and manage capacity

#### Acceptance Criteria

1. WHEN an Organizer requests registrations from `/api/workshop/registrations`, THE Workshop_API SHALL return all registrations with a 200 status
2. THE Workshop_API SHALL return an empty list when no registrations exist
3. THE Workshop_API SHALL include registration details: Registration_ID, Workshop_ID, participant information, and registration timestamp

### Requirement 8: Request Validation

**User Story:** As a system administrator, I want invalid requests to be rejected with clear error messages, so that clients can correct their requests

#### Acceptance Criteria

1. WHEN a request contains malformed JSON, THE Workshop_API SHALL return a 400 status with an error message
2. WHEN a request is missing required fields, THE Workshop_API SHALL return a 400 status listing the missing fields
3. WHEN a request contains invalid data types, THE Workshop_API SHALL return a 400 status describing the type mismatch
4. THE Workshop_API SHALL include descriptive error messages in all error responses

### Requirement 9: Data Persistence with JSON File

**User Story:** As an Organizer, I want workshop data to persist across server restarts, so that data is not lost

#### Acceptance Criteria

1. WHEN the Workshop_API creates or updates a Workshop, THE Workshop_Store SHALL persist the changes to a JSON file in the project directory
2. WHEN the Workshop_API creates a Challenge, THE Workshop_Store SHALL persist the Challenge to the JSON file
3. WHEN the Workshop_API creates a Registration, THE Workshop_Store SHALL persist the Registration to the JSON file
4. WHEN the Workshop_API restarts, THE Workshop_Store SHALL restore all previously created workshops, challenges, and registrations from the JSON file
5. THE Workshop_Store SHALL maintain data consistency across all operations

### Requirement 10: API Response Format

**User Story:** As a client developer, I want consistent JSON responses, so that I can reliably parse API responses

#### Acceptance Criteria

1. THE Workshop_API SHALL return all responses in JSON format
2. THE Workshop_API SHALL include a Content-Type header of application/json in all responses
3. THE Workshop_API SHALL use consistent field names across all endpoints
4. THE Workshop_API SHALL represent timestamps in ISO 8601 format

### Requirement 11: Technology Stack

**User Story:** As a developer, I want the backend implemented with specific technologies, so that the system meets technical requirements

#### Acceptance Criteria

1. THE Workshop_API SHALL be implemented using Python
2. THE Workshop_API SHALL use the Flask framework for HTTP request handling
3. THE Workshop_Store SHALL use JSON file format for data persistence
4. THE Workshop_Store SHALL store the JSON file in the project directory
