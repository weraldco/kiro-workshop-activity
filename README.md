# Workshop Management API

A Flask-based REST API for managing workshops, challenges, and participant registrations with JSON file persistence.

## Features

- Create and manage workshops with capacity limits
- Add challenges to workshops
- Register participants with automatic capacity enforcement
- Thread-safe JSON file persistence
- Comprehensive input validation
- RESTful API design with standardized responses

## Requirements

- Python 3.8+
- Flask
- pytest (for testing)
- hypothesis (for property-based testing)

## Installation

1. Clone the repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask development server:

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

All responses follow a standardized format:

**Success Response:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error description",
  "data": {}
}
```

### Workshop Endpoints

#### Create Workshop
```bash
POST /api/workshop
```

**Request Body:**
```json
{
  "title": "Python Workshop",
  "description": "Learn Python basics",
  "start_time": "2024-03-01T10:00:00Z",
  "end_time": "2024-03-01T16:00:00Z",
  "capacity": 20,
  "delivery_mode": "online"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "start_time": "2024-03-01T10:00:00Z",
    "end_time": "2024-03-01T16:00:00Z",
    "capacity": 20,
    "delivery_mode": "online",
    "registration_count": 0
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/workshop \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "start_time": "2024-03-01T10:00:00Z",
    "end_time": "2024-03-01T16:00:00Z",
    "capacity": 20,
    "delivery_mode": "online"
  }'
```

#### List All Workshops
```bash
GET /api/workshop
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Python Workshop",
      ...
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/workshop
```

#### Get Specific Workshop
```bash
GET /api/workshop/{workshop_id}
```

**Response:** `200 OK` or `404 Not Found`

**Example:**
```bash
curl http://localhost:5000/api/workshop/550e8400-e29b-41d4-a716-446655440000
```

### Challenge Endpoints

#### Create Challenge
```bash
POST /api/workshop/{workshop_id}/challenge
```

**Request Body:**
```json
{
  "title": "Build a Calculator",
  "description": "Create a simple calculator app"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Build a Calculator",
    "description": "Create a simple calculator app",
    "created_at": "2024-02-26T12:00:00Z"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/workshop/550e8400-e29b-41d4-a716-446655440000/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build a Calculator",
    "description": "Create a simple calculator app"
  }'
```

### Registration Endpoints

#### Register for Workshop
```bash
POST /api/workshop/{workshop_id}/register
```

**Request Body:**
```json
{
  "participant_name": "John Doe",
  "participant_email": "john@example.com"
}
```

**Response:** `201 Created` or `409 Conflict` (if full)
```json
{
  "success": true,
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
    "participant_name": "John Doe",
    "participant_email": "john@example.com",
    "registered_at": "2024-02-26T12:30:00Z"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/workshop/550e8400-e29b-41d4-a716-446655440000/register \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "John Doe",
    "participant_email": "john@example.com"
  }'
```

#### List All Registrations
```bash
GET /api/workshop/registrations
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
      "participant_name": "John Doe",
      "participant_email": "john@example.com",
      "registered_at": "2024-02-26T12:30:00Z"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/workshop/registrations
```

## Validation Rules

### Workshop Creation
- `title`: Non-empty string (required)
- `start_time`: Must be before `end_time` (required)
- `capacity`: Positive integer (required)
- `delivery_mode`: Must be "online", "face-to-face", or "hybrid" (required)

### Challenge Creation
- `title`: Non-empty string (required)
- Workshop must exist

### Registration
- `participant_name`: Required
- `participant_email`: Required
- Workshop must exist
- Workshop must have available capacity

## Error Codes

- `400 Bad Request`: Invalid input data or validation failure
- `404 Not Found`: Resource (workshop) does not exist
- `409 Conflict`: Workshop is at capacity
- `500 Internal Server Error`: Unexpected server error

## Data Persistence

Workshop data is stored in `workshop_data.json` in the project root directory. The file is created automatically on first use and uses file locking for thread-safe concurrent access.

## Testing

Run all tests:
```bash
pytest
```

Run specific test suites:
```bash
# Unit tests
pytest tests/unit/

# Property-based tests
pytest tests/property/

# Integration tests
pytest tests/integration/
```

## Project Structure

```
.
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── validators.py         # Input validation
│   ├── routes/
│   │   └── workshop_routes.py
│   ├── services/
│   │   ├── workshop_service.py
│   │   ├── challenge_service.py
│   │   └── registration_service.py
│   └── store/
│       ├── file_lock.py
│       └── workshop_store.py
├── tests/
│   ├── unit/
│   ├── property/
│   └── integration/
├── run.py                    # Application entry point
├── requirements.txt
└── workshop_data.json        # Data file (auto-generated)
```

## Development

The application uses a three-layer architecture:
- **API Layer**: Flask routes handle HTTP requests/responses
- **Business Logic Layer**: Services implement workshop management logic
- **Data Access Layer**: Store handles JSON file persistence with locking

## License

This project is provided as-is for educational purposes.
