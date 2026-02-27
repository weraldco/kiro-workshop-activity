# Workshop Management System - API Endpoints

This document lists all available API endpoints in the Workshop Management System backend.

## Base URL
```
http://localhost:3001
```

## Health Check

### GET /health
Check if the API server is running.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

---

## Workshop Endpoints

### POST /api/workshops
Create a new workshop with default status='pending' and signup_enabled=true.

**Request Body:**
```json
{
  "title": "Workshop Title",
  "description": "Workshop Description"
}
```

**Response (201):**
```json
{
  "id": "uuid-v4",
  "title": "Workshop Title",
  "description": "Workshop Description",
  "status": "pending",
  "signup_enabled": true,
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

---

### GET /api/workshops
List all workshops.

**Response (200):**
```json
{
  "workshops": [
    {
      "id": "uuid-v4",
      "title": "Workshop Title",
      "description": "Workshop Description",
      "status": "pending",
      "signup_enabled": true,
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

---

### PATCH /api/workshops/:id/status
Update workshop status (pending → ongoing → completed).

**Request Body:**
```json
{
  "status": "ongoing"
}
```

**Response (200):**
```json
{
  "id": "uuid-v4",
  "title": "Workshop Title",
  "description": "Workshop Description",
  "status": "ongoing",
  "signup_enabled": true,
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

---

### PATCH /api/workshops/:id/signup-flag
Toggle signup_enabled flag.

**Request Body:**
```json
{
  "signup_enabled": false
}
```

**Response (200):**
```json
{
  "id": "uuid-v4",
  "title": "Workshop Title",
  "description": "Workshop Description",
  "status": "pending",
  "signup_enabled": false,
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

---

## Participant Endpoints

### POST /api/workshops/:id/signup
Register a participant for a workshop.

**Requirements:**
- Workshop status must be 'pending'
- Workshop signup_enabled must be true
- User cannot sign up twice for the same workshop

**Request Body:**
```json
{
  "user_id": "user123"
}
```

**Response (200):**
```json
{
  "success": true,
  "participant_id": "uuid-v4"
}
```

**Error Response (403):**
```json
{
  "error": "Signups are not allowed for workshops with status 'ongoing'",
  "code": "SIGNUP_NOT_ALLOWED",
  "status": 403
}
```

---

### GET /api/workshops/:id/participants
List all participants for a workshop.

**Response (200):**
```json
{
  "participants": [
    {
      "id": "uuid-v4",
      "workshop_id": "uuid-v4",
      "user_id": "user123",
      "signed_up_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

---

## Challenge Endpoints

### POST /api/workshops/:id/challenges
Create a challenge for a workshop.

**Requirements:**
- Workshop must exist
- Title: 1-200 characters
- Description: 1-1000 characters
- HTML content must be valid

**Request Body:**
```json
{
  "title": "Challenge Title",
  "description": "Challenge Description",
  "html_content": "<p>Challenge content in HTML</p>"
}
```

**Response (201):**
```json
{
  "success": true,
  "challenge_id": "uuid-v4",
  "challenge": {
    "id": "uuid-v4",
    "workshop_id": "uuid-v4",
    "title": "Challenge Title",
    "description": "Challenge Description",
    "html_content": "<p>Challenge content in HTML</p>"
  }
}
```

---

### GET /api/workshops/:id/challenges
List challenges for a workshop with access control.

**Requirements:**
- Workshop status must be 'ongoing'
- User must be a signed-up participant
- user_id query parameter is required

**Query Parameters:**
- `user_id` (required): The user requesting access

**Response (200):**
```json
{
  "challenges": [
    {
      "id": "uuid-v4",
      "workshop_id": "uuid-v4",
      "title": "Challenge Title",
      "description": "Challenge Description",
      "html_content": "<p>Challenge content in HTML</p>"
    }
  ]
}
```

**Error Response (403):**
```json
{
  "error": "Challenges are not accessible for pending workshops",
  "code": "CHALLENGE_ACCESS_DENIED",
  "status": 403
}
```

---

### GET /api/challenges/:id
Get challenge details with access control.

**Requirements:**
- Workshop status must be 'ongoing'
- User must be a signed-up participant
- user_id query parameter is required

**Query Parameters:**
- `user_id` (required): The user requesting access

**Response (200):**
```json
{
  "challenge": {
    "id": "uuid-v4",
    "workshop_id": "uuid-v4",
    "title": "Challenge Title",
    "description": "Challenge Description",
    "html_content": "<p>Challenge content in HTML</p>"
  }
}
```

**Error Response (403):**
```json
{
  "error": "Only participants can access challenges",
  "code": "CHALLENGE_ACCESS_DENIED",
  "status": 403
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Human-readable error message",
  "code": "MACHINE_READABLE_ERROR_CODE",
  "status": 400
}
```

### Common Error Codes:
- `VALIDATION_ERROR` (400): Invalid request data
- `WORKSHOP_NOT_FOUND` (404): Workshop does not exist
- `CHALLENGE_NOT_FOUND` (404): Challenge does not exist
- `NOT_FOUND` (404): Endpoint does not exist
- `SIGNUP_NOT_ALLOWED` (403): Signup is not permitted
- `DUPLICATE_SIGNUP` (403): User already signed up
- `CHALLENGE_ACCESS_DENIED` (403): Challenge access not allowed
- `DATABASE_ERROR` (500): Database operation failed
- `INTERNAL_ERROR` (500): Unexpected server error

---

## Middleware

The API includes the following middleware:

1. **CORS**: Enabled for all origins
2. **JSON Body Parser**: Parses JSON request bodies
3. **URL Encoded Parser**: Parses URL-encoded request bodies
4. **Request Logging**: Logs all incoming requests with timestamp
5. **Error Handler**: Global error handler for unhandled errors
6. **404 Handler**: Returns proper error for non-existent endpoints

---

## Testing

Run all tests:
```bash
npm test
```

Run integration tests:
```bash
npm test -- integration.test.ts
```

Run with coverage:
```bash
npm test:coverage
```

---

## Starting the Server

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm run build
npm start
```

The server will start on port 3001 by default (configurable via PORT environment variable).
