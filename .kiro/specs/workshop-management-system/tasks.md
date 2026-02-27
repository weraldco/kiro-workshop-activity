# Implementation Plan: Workshop Management System

## Overview

This implementation plan breaks down the Workshop Management System into incremental coding tasks. The system consists of a TypeScript/Node.js backend API with JSON database persistence and a Next.js frontend with TailwindCSS styling. Each task builds on previous work, starting with core infrastructure, then backend API implementation, followed by frontend development, and concluding with property-based testing using fast-check.

## Tasks

- [x] 1. Set up project structure and core infrastructure
  - Create backend directory structure (src/controllers, src/services, src/types, src/database)
  - Create frontend directory structure (pages, components, lib)
  - Define TypeScript interfaces for Workshop, Participant, Challenge, and API responses
  - Set up package.json with dependencies (Next.js, TailwindCSS, fast-check, Jest, uuid)
  - Configure TypeScript (tsconfig.json) for both backend and frontend
  - Initialize JSON database files (workshops.json, participants.json, challenges.json) with empty arrays
  - _Requirements: 4.1, 4.2, 4.3, 4.5, 9.1, 9.2, 9.3_

- [x] 2. Implement Database Service layer
  - [x] 2.1 Create Database Service with atomic read/write operations
    - Implement readWorkshops(), writeWorkshops(), readParticipants(), writeParticipants(), readChallenges(), writeChallenges()
    - Add file system error handling and atomic write operations
    - _Requirements: 1.5, 4.5, 5.5, 6.5_
  
  - [ ]* 2.2 Write property test for Database Service
    - **Property 11: Database Persistence Round Trip**
    - **Validates: Requirements 1.5, 4.5, 5.5, 6.5**
  
  - [x] 2.3 Add schema validation functions
    - Implement validation for Workshop schema (UUID, title length, description length, status enum, timestamps)
    - Implement validation for Participant schema (UUID, workshop_id reference, user_id, timestamp)
    - Implement validation for Challenge schema (UUID, workshop_id reference, title/description lengths, HTML content)
    - _Requirements: 4.1, 4.2, 4.3, 5.1, 5.2, 5.3_
  
  - [ ]* 2.4 Write property tests for schema validation
    - **Property 1: Workshop Status Enum Constraint**
    - **Property 7: Workshop Schema Completeness**
    - **Property 8: Participant Schema Completeness**
    - **Property 9: Challenge Schema Completeness**
    - **Property 12: Challenge Field Length Constraints**
    - **Property 13: HTML Content Validation**
    - **Validates: Requirements 1.1, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 6.1_
  
  - [x] 2.5 Implement referential integrity checks
    - Add function to verify workshop_id exists before creating participants or challenges
    - Add function to check for dependent records before deletion
    - _Requirements: 4.4, 5.4_
  
  - [ ]* 2.6 Write property test for referential integrity
    - **Property 10: Referential Integrity**
    - **Validates: Requirements 4.4, 5.4**

- [x] 3. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Implement Access Control Service
  - [x] 4.1 Create Access Control Service with authorization logic
    - Implement canSignup(workshop) - check status='pending' AND signup_enabled=true
    - Implement canAccessChallenges(workshop, userId) - check status='ongoing' AND user is participant
    - Implement isParticipant(workshopId, userId) - check participant list membership
    - _Requirements: 1.3, 2.1, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 6.2, 6.3_
  
  - [ ]* 4.2 Write property tests for access control rules
    - **Property 3: Signup Eligibility Rule**
    - **Property 5: Challenge Visibility Rule**
    - **Property 6: Non-Participant Challenge Access Denial**
    - **Validates: Requirements 1.3, 1.4, 2.1, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 6.2, 6.3**

- [x] 5. Implement Workshop Controller and API endpoints
  - [x] 5.1 Create Workshop Controller with CRUD operations
    - Implement POST /api/workshops - create workshop with default status='pending' and signup_enabled=true
    - Implement GET /api/workshops - list all workshops
    - Implement PATCH /api/workshops/:id/status - update workshop status
    - Implement PATCH /api/workshops/:id/signup-flag - toggle signup_enabled flag
    - Add request validation and error responses (400, 404, 500)
    - _Requirements: 1.1, 1.2, 1.5, 6.1, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 9.4_
  
  - [ ]* 5.2 Write property tests for workshop operations
    - **Property 2: Default Workshop State**
    - **Property 14: Workshop List Response Format**
    - **Validates: Requirements 1.2, 6.4, 7.2, 7.3**
  
  - [ ]* 5.3 Write unit tests for Workshop Controller
    - Test workshop creation with valid data
    - Test status transitions (pending → ongoing → completed)
    - Test invalid status values rejected
    - Test empty workshop list returns empty array
    - _Requirements: 1.1, 1.2, 1.5, 7.4_

- [x] 6. Implement Participant Controller and signup endpoints
  - [x] 6.1 Create Participant Controller with signup operations
    - Implement POST /api/workshops/:id/signup - register participant with access control checks
    - Implement GET /api/workshops/:id/participants - list participants for a workshop
    - Add duplicate signup prevention (uniqueness constraint on workshop_id + user_id)
    - Add error responses for forbidden signups (403) and validation errors (400)
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [ ]* 6.2 Write property tests for participant operations
    - **Property 4: Signup Effect on Participant List**
    - **Property 17: Participant Uniqueness Constraint**
    - **Validates: Requirements 2.2**
  
  - [ ]* 6.3 Write unit tests for Participant Controller
    - Test successful signup for pending workshop with signup_enabled=true
    - Test rejected signup for ongoing workshop
    - Test rejected signup for completed workshop
    - Test rejected signup when signup_enabled=false
    - Test duplicate signup rejection
    - _Requirements: 2.1, 2.3, 2.4_

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement Challenge Controller and API endpoints
  - [x] 8.1 Create Challenge Controller with CRUD and access control
    - Implement POST /api/workshops/:id/challenges - create challenge with validation
    - Implement GET /api/workshops/:id/challenges - list challenges with access control (only for ongoing workshops and participants)
    - Implement GET /api/challenges/:id - get challenge details with access control
    - Add validation for title (max 200 chars), description (max 1000 chars), and HTML content
    - Add authorization checks using Access Control Service
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ]* 8.2 Write unit tests for Challenge Controller
    - Test challenge creation with valid data
    - Test challenge access allowed for ongoing workshop participant
    - Test challenge access denied for pending workshop
    - Test challenge access denied for completed workshop
    - Test challenge access denied for non-participant
    - Test title length validation (accept ≤200, reject >200)
    - Test description length validation (accept ≤1000, reject >1000)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 5.1, 5.2_

- [x] 9. Implement Next.js frontend structure
  - [x] 9.1 Set up Next.js pages and TailwindCSS configuration
    - Create pages/index.tsx for workshop listing page
    - Configure TailwindCSS in tailwind.config.js and globals.css
    - Set up Next.js API route configuration (if needed for proxying)
    - _Requirements: 9.1, 9.2, 9.5_
  
  - [x] 9.2 Create API client module
    - Implement lib/api.ts with fetchWorkshops() function
    - Add HTTP error handling and response parsing
    - Add retry logic for transient failures
    - _Requirements: 9.5_
  
  - [ ]* 9.3 Write unit tests for API client
    - Test successful API response parsing
    - Test network error handling
    - Test timeout error handling
    - _Requirements: 9.5_

- [x] 10. Implement frontend components
  - [x] 10.1 Create WorkshopCard component
    - Implement component with props: workshop (Workshop interface)
    - Display title, description, and status with TailwindCSS styling
    - Add status-specific styling (different colors for pending/ongoing/completed)
    - Show signup availability indicator based on signup_enabled
    - _Requirements: 8.1, 8.3, 9.2_
  
  - [x] 10.2 Create WorkshopList component
    - Implement component with state: workshops array, loading boolean, error string
    - Fetch workshops from API on component mount
    - Render WorkshopCard for each workshop
    - Display loading state while fetching
    - Display error message when API fails
    - _Requirements: 8.1, 8.2, 8.5, 9.2_
  
  - [ ]* 10.3 Write property tests for frontend rendering
    - **Property 15: Frontend Workshop Rendering Completeness**
    - **Property 16: Frontend Error Display**
    - **Validates: Requirements 8.1, 8.3, 8.5**
  
  - [ ]* 10.4 Write unit tests for frontend components
    - Test WorkshopCard renders all fields correctly
    - Test WorkshopList displays workshops after successful fetch
    - Test WorkshopList displays error message on API failure
    - Test WorkshopList displays loading state
    - _Requirements: 8.1, 8.3, 8.5_

- [x] 11. Integration and wiring
  - [x] 11.1 Wire all backend components together
    - Connect controllers to services and database layer
    - Set up Express or Next.js API routes for all endpoints
    - Add middleware for error handling and request logging
    - Verify all API endpoints are accessible
    - _Requirements: 9.4_
  
  - [x] 11.2 Wire frontend to backend API
    - Update API client with correct backend URL
    - Integrate WorkshopList component into pages/index.tsx
    - Test end-to-end flow: frontend fetch → backend API → database → response
    - _Requirements: 8.2, 9.5_
  
  - [ ]* 11.3 Write integration tests
    - Test complete signup flow (API request → database update → response)
    - Test complete challenge access flow (API request → access control → response)
    - Test workshop status transition flow
    - _Requirements: 1.3, 2.1, 3.1_

- [x] 12. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use fast-check library with minimum 100 iterations
- All 17 correctness properties from the design document have corresponding test tasks
- Checkpoints ensure incremental validation throughout implementation
- Backend uses TypeScript with Node.js runtime
- Frontend uses Next.js with TypeScript and TailwindCSS
- Database uses JSON files for simple persistence without external dependencies
