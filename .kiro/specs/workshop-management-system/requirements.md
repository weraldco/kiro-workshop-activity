# Requirements Document

## Introduction

The Workshop Management System is a backend API with frontend integration that enables organizers to create and manage workshops with different lifecycle states. The system controls participant signup availability and challenge visibility based on workshop status. The backend uses a JSON database for persistence, and the frontend is built with Next.js and TailwindCSS to display workshop listings.

## Glossary

- **Workshop_Management_API**: The backend REST API that handles workshop operations and data persistence
- **Workshop_Database**: The JSON-based database storing workshop data, participant information, and challenges
- **Workshop**: A managed event with a status, participant list, and associated challenges
- **Workshop_Status**: The current lifecycle state of a workshop (pending, ongoing, or completed)
- **Organizer**: A user role with permissions to create and manage workshops
- **Participant**: A user who can sign up for workshops and view challenges
- **Challenge**: Content associated with a workshop, including title, description, and HTML text
- **Signup_Flag**: A boolean configuration that controls whether participants can register for a workshop
- **Workshop_Frontend**: The Next.js application that displays workshop information to users

## Requirements

### Requirement 1: Workshop Status Management

**User Story:** As an organizer, I want to manage workshop status transitions, so that I can control participant access throughout the workshop lifecycle

#### Acceptance Criteria

1. THE Workshop_Management_API SHALL support three Workshop_Status values: pending, ongoing, and completed
2. WHEN an Organizer creates a Workshop, THE Workshop_Management_API SHALL set the Workshop_Status to pending
3. WHEN an Organizer changes Workshop_Status from pending to ongoing, THE Workshop_Management_API SHALL prevent new Participant signups
4. WHEN an Organizer changes Workshop_Status to completed, THE Workshop_Management_API SHALL prevent Participant access to Challenges
5. THE Workshop_Management_API SHALL persist Workshop_Status changes to the Workshop_Database

### Requirement 2: Participant Signup Control for Pending Workshops

**User Story:** As a participant, I want to sign up for pending workshops, so that I can register my attendance

#### Acceptance Criteria

1. WHILE Workshop_Status is pending, THE Workshop_Management_API SHALL accept Participant signup requests
2. WHEN a Participant submits a signup request for a pending Workshop, THE Workshop_Management_API SHALL add the Participant to the Workshop participant list
3. WHILE Workshop_Status is ongoing, THE Workshop_Management_API SHALL reject Participant signup requests
4. WHILE Workshop_Status is completed, THE Workshop_Management_API SHALL reject Participant signup requests

### Requirement 3: Challenge Visibility Control

**User Story:** As a participant, I want to access challenges during ongoing workshops, so that I can participate in workshop activities

#### Acceptance Criteria

1. WHILE Workshop_Status is ongoing, THE Workshop_Management_API SHALL provide Challenge access to signed-up Participants
2. WHILE Workshop_Status is pending, THE Workshop_Management_API SHALL deny Challenge access to all Participants
3. WHILE Workshop_Status is completed, THE Workshop_Management_API SHALL deny Challenge access to all Participants
4. WHEN a non-signed-up Participant requests Challenge access, THE Workshop_Management_API SHALL return an authorization error

### Requirement 4: Workshop Database Schema

**User Story:** As an organizer, I want workshop data persisted in a structured format, so that workshop information is reliably stored and retrieved

#### Acceptance Criteria

1. THE Workshop_Database SHALL store Workshop records with the following fields: id, title, description, status, signup_enabled, created_at, updated_at
2. THE Workshop_Database SHALL store Participant records with the following fields: id, workshop_id, user_id, signed_up_at
3. THE Workshop_Database SHALL store Challenge records with the following fields: id, workshop_id, title, description, html_content
4. THE Workshop_Database SHALL maintain referential relationships between Workshop, Participant, and Challenge records
5. THE Workshop_Database SHALL use JSON format for data persistence

### Requirement 5: Challenge Content Management

**User Story:** As an organizer, I want to create challenges with rich content, so that participants receive detailed workshop materials

#### Acceptance Criteria

1. WHEN an Organizer creates a Challenge, THE Workshop_Management_API SHALL accept a title field with maximum length of 200 characters
2. WHEN an Organizer creates a Challenge, THE Workshop_Management_API SHALL accept a description field with maximum length of 1000 characters
3. WHEN an Organizer creates a Challenge, THE Workshop_Management_API SHALL accept an html_content field containing valid HTML
4. THE Workshop_Management_API SHALL associate each Challenge with exactly one Workshop
5. THE Workshop_Management_API SHALL persist Challenge data to the Workshop_Database

### Requirement 6: Signup Flag Control

**User Story:** As an organizer, I want to manually enable or disable signups, so that I have fine-grained control over workshop registration

#### Acceptance Criteria

1. THE Workshop_Management_API SHALL maintain a Signup_Flag for each Workshop
2. WHEN an Organizer sets Signup_Flag to false, THE Workshop_Management_API SHALL reject all Participant signup requests regardless of Workshop_Status
3. WHEN an Organizer sets Signup_Flag to true AND Workshop_Status is pending, THE Workshop_Management_API SHALL accept Participant signup requests
4. WHEN an Organizer creates a Workshop, THE Workshop_Management_API SHALL set Signup_Flag to true by default
5. THE Workshop_Management_API SHALL persist Signup_Flag changes to the Workshop_Database

### Requirement 7: Workshop Listing API Endpoint

**User Story:** As a frontend application, I want to retrieve all workshops, so that I can display workshop information to users

#### Acceptance Criteria

1. THE Workshop_Management_API SHALL provide a GET endpoint that returns all Workshop records
2. WHEN the Workshop_Frontend requests the workshop list, THE Workshop_Management_API SHALL return Workshop data including id, title, description, status, and signup_enabled fields
3. THE Workshop_Management_API SHALL return workshop list data in JSON format
4. WHEN the Workshop_Database contains no workshops, THE Workshop_Management_API SHALL return an empty array
5. THE Workshop_Management_API SHALL respond to workshop list requests within 500 milliseconds

### Requirement 8: Frontend Workshop Display

**User Story:** As a user, I want to view available workshops in a web interface, so that I can browse workshop offerings

#### Acceptance Criteria

1. THE Workshop_Frontend SHALL display a list of all workshops retrieved from the Workshop_Management_API
2. WHEN the Workshop_Frontend loads, THE Workshop_Frontend SHALL make a GET request to the workshop listing endpoint
3. THE Workshop_Frontend SHALL display each Workshop with its title, description, and status
4. THE Workshop_Frontend SHALL use TailwindCSS for styling workshop list components
5. WHEN the Workshop_Management_API returns an error, THE Workshop_Frontend SHALL display an error message to the user

### Requirement 9: Technology Stack Implementation

**User Story:** As a developer, I want the system built with specified technologies, so that it meets architectural requirements

#### Acceptance Criteria

1. THE Workshop_Frontend SHALL be implemented using the Next.js framework
2. THE Workshop_Frontend SHALL use TailwindCSS for styling
3. THE Workshop_Management_API SHALL use a JSON-based database for data persistence
4. THE Workshop_Management_API SHALL expose RESTful HTTP endpoints
5. THE Workshop_Frontend SHALL communicate with the Workshop_Management_API using HTTP requests
