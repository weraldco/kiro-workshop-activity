# API Documentation

Complete API reference for the Workshop Management System.

## Base URL

```
http://localhost:3535/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access-token>
```

Tokens expire after 30 minutes and must be refreshed by logging in again.

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint**: `POST /api/auth/register`

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Validation Rules**:
- Email: Valid email format, unique
- Password: Min 8 chars, must contain uppercase, lowercase, number, and special character
- Name: 2-100 characters

**Success Response** (201):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

**Error Responses**:
- `400` - Validation error
- `409` - Email already exists

---

### Login

Authenticate and receive access token.

**Endpoint**: `POST /api/auth/login`

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

**Error Responses**:
- `400` - Missing credentials
- `401` - Invalid credentials

---

### Get Current User

Get authenticated user's information.

**Endpoint**: `GET /api/auth/me`

**Authentication**: Required

**Success Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses**:
- `401` - Unauthorized (missing or invalid token)

---

## Workshop Endpoints

### Create Workshop

Create a new workshop (owner).

**Endpoint**: `POST /api/workshops`

**Authentication**: Required

**Request Body**:
```json
{
  "title": "Python Workshop",
  "description": "Learn Python basics"
}
```

**Validation Rules**:
- Title: Required, max 200 characters
- Description: Required, max 1000 characters

**Success Response** (201):
```json
{
  "id": "uuid",
  "title": "Python Workshop",
  "description": "Learn Python basics",
  "status": "pending",
  "signup_enabled": true,
  "owner_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses**:
- `400` - Validation error
- `401` - Unauthorized

---

### List All Workshops

Get all workshops (public).

**Endpoint**: `GET /api/workshops`

**Authentication**: Optional

**Success Response** (200):
```json
[
  {
    "id": "uuid",
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "status": "ongoing",
    "signup_enabled": true,
    "owner_id": "uuid",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get My Workshops

Get workshops owned by current user.

**Endpoint**: `GET /api/workshops/my`

**Authentication**: Required

**Success Response** (200):
```json
[
  {
    "id": "uuid",
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "status": "ongoing",
    "signup_enabled": true,
    "owner_id": "uuid",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

**Error Responses**:
- `401` - Unauthorized

---

### Get Workshop by ID

Get workshop details.

**Endpoint**: `GET /api/workshops/:id`

**Authentication**: Optional

**Success Response** (200):
```json
{
  "id": "uuid",
  "title": "Python Workshop",
  "description": "Learn Python basics",
  "status": "ongoing",
  "signup_enabled": true,
  "owner_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses**:
- `404` - Workshop not found

---

### Update Workshop

Update workshop details (owner only).

**Endpoint**: `PATCH /api/workshops/:id`

**Authentication**: Required (owner only)

**Request Body** (all fields optional):
```json
{
  "title": "Advanced Python Workshop",
  "description": "Deep dive into Python",
  "status": "ongoing",
  "signup_enabled": false
}
```

**Status Values**: `pending`, `ongoing`, `completed`

**Success Response** (200):
```json
{
  "id": "uuid",
  "title": "Advanced Python Workshop",
  "description": "Deep dive into Python",
  "status": "ongoing",
  "signup_enabled": false,
  "owner_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

**Error Responses**:
- `400` - Validation error
- `401` - Unauthorized
- `403` - Not workshop owner
- `404` - Workshop not found

---

### Delete Workshop

Delete workshop (owner only).

**Endpoint**: `DELETE /api/workshops/:id`

**Authentication**: Required (owner only)

**Success Response** (204):
No content

**Error Responses**:
- `401` - Unauthorized
- `403` - Not workshop owner
- `404` - Workshop not found

---

## Participant Endpoints

### Join Workshop

Request to join a workshop.

**Endpoint**: `POST /api/workshops/:id/join`

**Authentication**: Required

**Success Response** (201):
```json
{
  "id": "uuid",
  "workshop_id": "uuid",
  "user_id": "uuid",
  "status": "pending",
  "requested_at": "2024-01-01T00:00:00Z",
  "approved_at": null,
  "approved_by": null,
  "user_name": "John Doe",
  "user_email": "user@example.com"
}
```

**Error Responses**:
- `400` - Owner cannot join own workshop
- `401` - Unauthorized
- `404` - Workshop not found
- `409` - Already joined

---

### Get Workshop Participants

Get participants for a workshop (owner only).

**Endpoint**: `GET /api/workshops/:id/participants`

**Authentication**: Required (owner only)

**Query Parameters**:
- `status` (optional): Filter by status (`pending`, `joined`, `rejected`, `waitlisted`)

**Success Response** (200):

Without filter (grouped by status):
```json
{
  "pending": [
    {
      "id": "uuid",
      "workshop_id": "uuid",
      "user_id": "uuid",
      "status": "pending",
      "requested_at": "2024-01-01T00:00:00Z",
      "approved_at": null,
      "approved_by": null,
      "user_name": "John Doe",
      "user_email": "user@example.com"
    }
  ],
  "joined": [...],
  "rejected": [...],
  "waitlisted": [...]
}
```

With filter:
```json
[
  {
    "id": "uuid",
    "workshop_id": "uuid",
    "user_id": "uuid",
    "status": "joined",
    "requested_at": "2024-01-01T00:00:00Z",
    "approved_at": "2024-01-02T00:00:00Z",
    "approved_by": "uuid",
    "user_name": "John Doe",
    "user_email": "user@example.com"
  }
]
```

**Error Responses**:
- `401` - Unauthorized
- `403` - Not workshop owner
- `404` - Workshop not found

---

### Update Participant Status

Approve, reject, or waitlist a participant (owner only).

**Endpoint**: `PATCH /api/workshops/:workshop_id/participants/:participant_id`

**Authentication**: Required (owner only)

**Request Body**:
```json
{
  "status": "joined"
}
```

**Status Values**: `pending`, `joined`, `rejected`, `waitlisted`

**Success Response** (200):
```json
{
  "id": "uuid",
  "workshop_id": "uuid",
  "user_id": "uuid",
  "status": "joined",
  "requested_at": "2024-01-01T00:00:00Z",
  "approved_at": "2024-01-02T00:00:00Z",
  "approved_by": "uuid",
  "user_name": "John Doe",
  "user_email": "user@example.com"
}
```

**Error Responses**:
- `400` - Invalid status or missing status
- `401` - Unauthorized
- `403` - Not workshop owner
- `404` - Workshop or participant not found

---

### Remove Participant

Remove participant from workshop (owner or self).

**Endpoint**: `DELETE /api/workshops/:workshop_id/participants/:participant_id`

**Authentication**: Required (owner or participant)

**Success Response** (204):
No content

**Error Responses**:
- `401` - Unauthorized
- `403` - Not authorized (not owner or self)
- `404` - Workshop or participant not found

---

### Get Joined Workshops

Get workshops the current user has joined.

**Endpoint**: `GET /api/workshops/joined`

**Authentication**: Required

**Success Response** (200):
```json
[
  {
    "id": "uuid",
    "workshop_id": "uuid",
    "user_id": "uuid",
    "status": "joined",
    "requested_at": "2024-01-01T00:00:00Z",
    "approved_at": "2024-01-02T00:00:00Z",
    "approved_by": "uuid",
    "workshop_title": "Python Workshop",
    "workshop_description": "Learn Python basics",
    "workshop_status": "ongoing",
    "workshop_owner_id": "uuid"
  }
]
```

**Error Responses**:
- `401` - Unauthorized

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "status": 400
}
```

### Common Error Codes

- `VALIDATION_ERROR` - Input validation failed
- `MISSING_BODY` - Request body is required
- `UNAUTHORIZED` - Missing or invalid authentication
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `EMAIL_EXISTS` - Email already registered
- `ALREADY_JOINED` - Already joined workshop
- `OWNER_CANNOT_JOIN` - Workshop owners cannot join their own workshops
- `SERVER_ERROR` - Internal server error

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## Pagination

Currently not implemented. All list endpoints return all results.

For future implementation:
```
GET /api/workshops?page=1&limit=20
```

---

## Filtering and Sorting

Currently not implemented. For future implementation:

**Filtering**:
```
GET /api/workshops?status=ongoing&signup_enabled=true
```

**Sorting**:
```
GET /api/workshops?sort=created_at&order=desc
```

---

## Webhooks

Not currently implemented. For future implementation, consider webhooks for:
- New join request
- Join request approved/rejected
- Workshop status changed
- Participant removed

---

## API Versioning

Current version: v1 (implicit)

Future versions will use URL versioning:
```
/api/v2/workshops
```

---

## Testing the API

### Using curl

```bash
# Register
curl -X POST http://localhost:3535/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#","name":"Test User"}'

# Login
TOKEN=$(curl -X POST http://localhost:3535/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}' \
  | jq -r '.access_token')

# Create Workshop
curl -X POST http://localhost:3535/api/workshops \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Test Workshop","description":"Test description"}'
```

### Using Postman

1. Import the API collection (if available)
2. Set environment variable `base_url` to `http://localhost:3535`
3. Set environment variable `token` after login
4. Use `{{base_url}}` and `{{token}}` in requests

---

## Support

For API issues or questions:
- Check this documentation
- Review the code in `backend/app/routes/`
- Check test files for usage examples
- Create an issue on GitHub
