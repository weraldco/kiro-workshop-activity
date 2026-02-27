# Workshop Management API

A Flask-based REST API for managing workshops, challenges, and participant registrations with JSON file persistence.

## Features

- 🎯 Create and manage workshops with capacity limits
- 📝 Add challenges to workshops
- 👥 Register participants with automatic capacity enforcement
- 💾 Thread-safe JSON file persistence
- ✅ Comprehensive input validation
- 🔄 RESTful API design with standardized responses
- 🧪 68 automated tests (unit, property-based, integration)

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

### 1. Installation

Clone the repository or navigate to the project directory:

```bash
cd workshop-management-api
```

Create a virtual environment (recommended):

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Running the Application

Start the Flask development server:

```bash
python app.py
```

You should see output like:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:3535
```

The API is now available at `http://localhost:3535`

> **Note**: If port 3535 is in use, you can change it in `app.py` by modifying the `port` parameter in `app.run()`

### 3. Test the API

Open a new terminal and try creating a workshop:

```bash
curl -X POST http://localhost:3535/api/workshop \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "start_time": "2024-03-01T10:00:00",
    "end_time": "2024-03-01T16:00:00",
    "capacity": 20,
    "delivery_mode": "online"
  }'
```

You should receive a `201 Created` response with the workshop details.

## API Endpoints

All responses follow a standardized format for consistency and easy parsing.

### Response Format

**Success Response (HTTP 2xx):**
```json
{
  "success": true,
  "data": {
    // Response payload
  }
}
```

**Error Response (HTTP 4xx/5xx):**
```json
{
  "success": false,
  "error": "Human-readable error description",
  "data": {}
}
```

---

### Workshop Endpoints

#### 1. Create Workshop

Creates a new workshop with the specified details.

**Endpoint:** `POST /api/workshop`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Python Workshop",
  "description": "Learn Python basics",
  "start_time": "2024-03-01T10:00:00",
  "end_time": "2024-03-01T16:00:00",
  "capacity": 20,
  "delivery_mode": "online"
}
```

**Field Descriptions:**
- `title` (string, required): Workshop title, must be non-empty
- `description` (string, optional): Workshop description
- `start_time` (string, required): Start time in ISO 8601 format
- `end_time` (string, required): End time in ISO 8601 format (must be after start_time)
- `capacity` (integer, required): Maximum number of participants (must be positive)
- `delivery_mode` (string, required): One of "online", "face-to-face", or "hybrid"

**Success Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "start_time": "2024-03-01T10:00:00",
    "end_time": "2024-03-01T16:00:00",
    "capacity": 20,
    "delivery_mode": "online",
    "registration_count": 0
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (empty title, invalid time range, invalid capacity, invalid delivery mode)

**Example:**
```bash
curl -X POST http://localhost:3535/api/workshop \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "start_time": "2024-03-01T10:00:00",
    "end_time": "2024-03-01T16:00:00",
    "capacity": 20,
    "delivery_mode": "online"
  }'
```

---

#### 2. List All Workshops

Retrieves all workshops in the system.

**Endpoint:** `GET /api/workshop`

**Success Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Python Workshop",
      "description": "Learn Python basics",
      "start_time": "2024-03-01T10:00:00",
      "end_time": "2024-03-01T16:00:00",
      "capacity": 20,
      "delivery_mode": "online",
      "registration_count": 5
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:3535/api/workshop
```

---

#### 3. Get Specific Workshop

Retrieves details of a specific workshop by ID.

**Endpoint:** `GET /api/workshop/{workshop_id}`

**URL Parameters:**
- `workshop_id` (string, required): The unique workshop identifier

**Success Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Python Workshop",
    "description": "Learn Python basics",
    "start_time": "2024-03-01T10:00:00",
    "end_time": "2024-03-01T16:00:00",
    "capacity": 20,
    "delivery_mode": "online",
    "registration_count": 5
  }
}
```

**Error Responses:**
- `404 Not Found`: Workshop with the specified ID does not exist

**Example:**
```bash
curl http://localhost:3535/api/workshop/550e8400-e29b-41d4-a716-446655440000
```

---

### Challenge Endpoints

#### 4. Create Challenge

Creates a new challenge for a specific workshop.

**Endpoint:** `POST /api/workshop/{workshop_id}/challenge`

**URL Parameters:**
- `workshop_id` (string, required): The workshop identifier

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Build a Calculator",
  "description": "Create a simple calculator app"
}
```

**Field Descriptions:**
- `title` (string, required): Challenge title, must be non-empty
- `description` (string, optional): Challenge description

**Success Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Build a Calculator",
    "description": "Create a simple calculator app",
    "created_at": "2024-02-26T12:00:00+00:00"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (empty title)
- `404 Not Found`: Workshop does not exist

**Example:**
```bash
curl -X POST http://localhost:3535/api/workshop/550e8400-e29b-41d4-a716-446655440000/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build a Calculator",
    "description": "Create a simple calculator app"
  }'
```

---

### Registration Endpoints

#### 5. Register for Workshop

Registers a participant for a specific workshop.

**Endpoint:** `POST /api/workshop/{workshop_id}/register`

**URL Parameters:**
- `workshop_id` (string, required): The workshop identifier

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "participant_name": "John Doe",
  "participant_email": "john@example.com"
}
```

**Field Descriptions:**
- `participant_name` (string, required): Participant's full name
- `participant_email` (string, required): Participant's email address

**Success Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
    "participant_name": "John Doe",
    "participant_email": "john@example.com",
    "registered_at": "2024-02-26T12:30:00+00:00"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields
- `404 Not Found`: Workshop does not exist
- `409 Conflict`: Workshop is at full capacity

**Example:**
```bash
curl -X POST http://localhost:3535/api/workshop/550e8400-e29b-41d4-a716-446655440000/register \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "John Doe",
    "participant_email": "john@example.com"
  }'
```

---

#### 6. List All Registrations

Retrieves all registrations across all workshops.

**Endpoint:** `GET /api/workshop/registrations`

**Success Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
      "participant_name": "John Doe",
      "participant_email": "john@example.com",
      "registered_at": "2024-02-26T12:30:00+00:00"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:3535/api/workshop/registrations
```

---

## Complete API Workflow Example

Here's a complete workflow demonstrating all API endpoints:

```bash
# 1. Create a workshop
WORKSHOP_RESPONSE=$(curl -s -X POST http://localhost:3535/api/workshop \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python",
    "description": "Deep dive into Python",
    "start_time": "2024-04-15T09:00:00",
    "end_time": "2024-04-15T17:00:00",
    "capacity": 15,
    "delivery_mode": "hybrid"
  }')

# Extract workshop ID (requires jq)
WORKSHOP_ID=$(echo $WORKSHOP_RESPONSE | jq -r '.data.id')
echo "Created workshop: $WORKSHOP_ID"

# 2. List all workshops
curl http://localhost:3535/api/workshop

# 3. Get specific workshop
curl http://localhost:3535/api/workshop/$WORKSHOP_ID

# 4. Create a challenge
curl -X POST http://localhost:3535/api/workshop/$WORKSHOP_ID/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build a Web Scraper",
    "description": "Create a web scraper using BeautifulSoup"
  }'

# 5. Register participants
curl -X POST http://localhost:3535/api/workshop/$WORKSHOP_ID/register \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "Alice Smith",
    "participant_email": "alice@example.com"
  }'

curl -X POST http://localhost:3535/api/workshop/$WORKSHOP_ID/register \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "Bob Johnson",
    "participant_email": "bob@example.com"
  }'

# 6. List all registrations
curl http://localhost:3535/api/workshop/registrations
```

---

## Validation Rules

### Workshop Creation

| Field | Type | Required | Validation Rules |
|-------|------|----------|------------------|
| `title` | string | Yes | Must be non-empty (not blank or whitespace only) |
| `description` | string | No | Any string value |
| `start_time` | string | Yes | ISO 8601 format, must be before `end_time` |
| `end_time` | string | Yes | ISO 8601 format, must be after `start_time` |
| `capacity` | integer | Yes | Must be a positive integer (> 0) |
| `delivery_mode` | string | Yes | Must be one of: "online", "face-to-face", "hybrid" |

### Challenge Creation

| Field | Type | Required | Validation Rules |
|-------|------|----------|------------------|
| `title` | string | Yes | Must be non-empty (not blank or whitespace only) |
| `description` | string | No | Any string value |

### Registration

| Field | Type | Required | Validation Rules |
|-------|------|----------|------------------|
| `participant_name` | string | Yes | Must be provided |
| `participant_email` | string | Yes | Must be provided |

**Additional Registration Rules:**
- Workshop must exist (404 if not found)
- Workshop must have available capacity (409 if full)
- Registration count is automatically incremented

---

## HTTP Status Codes

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| `200 OK` | Success | GET requests return data successfully |
| `201 Created` | Resource created | POST requests create new resources successfully |
| `400 Bad Request` | Invalid input | Validation fails (empty title, invalid time range, invalid capacity, invalid delivery mode, missing fields, malformed JSON) |
| `404 Not Found` | Resource not found | Workshop ID does not exist |
| `409 Conflict` | Business rule violation | Workshop is at full capacity |
| `500 Internal Server Error` | Server error | Unexpected server error (file system issues, etc.) |

---

## Data Persistence

### Storage Location

Workshop data is persisted to a JSON file named `workshop_data.json` in the project root directory.

### File Structure

```json
{
  "workshops": [
    {
      "id": "...",
      "title": "...",
      "description": "...",
      "start_time": "...",
      "end_time": "...",
      "capacity": 20,
      "delivery_mode": "online",
      "registration_count": 5
    }
  ],
  "challenges": [
    {
      "id": "...",
      "workshop_id": "...",
      "title": "...",
      "description": "...",
      "created_at": "..."
    }
  ],
  "registrations": [
    {
      "id": "...",
      "workshop_id": "...",
      "participant_name": "...",
      "participant_email": "...",
      "registered_at": "..."
    }
  ]
}
```

### Thread Safety

The application uses file locking to ensure thread-safe concurrent access:
- All write operations acquire an exclusive lock
- Multiple read operations can occur simultaneously
- Prevents data corruption during concurrent requests

### Backup and Recovery

To backup your data:
```bash
cp workshop_data.json workshop_data_backup.json
```

To restore from backup:
```bash
cp workshop_data_backup.json workshop_data.json
```

To reset all data:
```bash
rm workshop_data.json
# File will be recreated on next API call
```

---

## Testing

### Run All Tests

```bash
pytest
```

Expected output:
```
68 passed in X.XXs
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/ -v

# Property-based tests only
pytest tests/property/ -v

# Integration tests only
pytest tests/integration/ -v
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Manual API Testing

A manual testing script is provided:

```bash
# Make sure the server is running first
python app.py

# In another terminal
python test_api_manual.py
```

---

## Troubleshooting

### Port Already in Use

**Problem:** Error message: "Address already in use" or "Port 3535 is in use"

**Solution 1:** Change the port in `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)  # Use different port
```

**Solution 2 (macOS):** Disable AirPlay Receiver which uses port 3535:
- System Settings → General → AirDrop & Handoff → Disable "AirPlay Receiver"

**Solution 3:** Find and kill the process using the port:
```bash
# Find process
lsof -i :3535

# Kill process (replace PID with actual process ID)
kill -9 PID
```

### Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'flask'` or similar

**Solution:** Make sure you've activated your virtual environment and installed dependencies:
```bash
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### JSON File Permission Error

**Problem:** Cannot read/write `workshop_data.json`

**Solution:** Check file permissions:
```bash
chmod 644 workshop_data.json
```

### Connection Refused

**Problem:** `curl: (7) Failed to connect to localhost port 3535: Connection refused`

**Solution:** Make sure the Flask server is running:
```bash
python app.py
```

Check the terminal for any error messages.

### Invalid JSON in Request

**Problem:** `400 Bad Request` with error about malformed JSON

**Solution:** Ensure your JSON is properly formatted:
- Use double quotes for strings (not single quotes)
- No trailing commas
- Proper escaping of special characters

**Valid:**
```bash
curl -X POST http://localhost:3535/api/workshop \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","capacity":10}'
```

**Invalid:**
```bash
curl -X POST http://localhost:3535/api/workshop \
  -H "Content-Type: application/json" \
  -d "{'title':'Test','capacity':10,}"  # Wrong quotes and trailing comma
```

### Tests Failing

**Problem:** Some tests fail when running `pytest`

**Solution:**
1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check if `workshop_data.json` is locked by another process
3. Delete test artifacts: `rm -rf .pytest_cache .hypothesis`
4. Run tests again: `pytest`

### Debug Mode Issues

**Problem:** Changes to code not reflected in running application

**Solution:** Flask debug mode should auto-reload. If not:
1. Stop the server (Ctrl+C)
2. Restart: `python app.py`
3. Verify debug mode is enabled in `app.py`: `debug=True`

---

## Project Structure

```
workshop-management-api/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── validators.py            # Input validation functions
│   ├── routes/
│   │   └── workshop_routes.py   # API route handlers
│   ├── services/
│   │   ├── workshop_service.py  # Workshop business logic
│   │   ├── challenge_service.py # Challenge business logic
│   │   └── registration_service.py # Registration business logic
│   └── store/
│       ├── file_lock.py         # File locking mechanism
│       └── workshop_store.py    # JSON file persistence
├── tests/
│   ├── unit/
│   │   ├── test_routes.py       # Route handler tests
│   │   ├── test_services.py     # Service layer tests
│   │   ├── test_store.py        # Data access tests
│   │   └── test_validators.py   # Validation tests
│   ├── property/
│   │   └── test_persistence_properties.py # Property-based tests
│   └── integration/
│       └── test_api_integration.py # End-to-end tests
├── app.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── workshop_data.json           # Data file (auto-generated)
└── .gitignore                   # Git ignore rules
```

---

## Architecture

The application follows a three-layer architecture for clean separation of concerns:

### 1. API Layer (Routes)
- Handles HTTP requests and responses
- Parses and validates request data
- Formats responses with standardized structure
- Maps HTTP status codes to business outcomes

### 2. Business Logic Layer (Services)
- Implements workshop management logic
- Enforces business rules (capacity limits, validation)
- Generates unique IDs and timestamps
- Coordinates between API and data layers

### 3. Data Access Layer (Store)
- Manages JSON file persistence
- Implements file locking for thread safety
- Provides CRUD operations for entities
- Handles data serialization/deserialization

**Benefits:**
- Easy to test each layer independently
- Clear separation of concerns
- Simple to modify or extend functionality
- Maintainable and scalable codebase

---

## CORS Configuration

The API is configured with CORS (Cross-Origin Resource Sharing) to allow frontend applications to communicate with the backend.

### Development CORS Settings

The following origins are allowed in development:
- `http://localhost:3000` (Create React App default)
- `http://localhost:5173` (Vite default)

Allowed methods: GET, POST, PATCH, PUT, DELETE, OPTIONS
Allowed headers: Content-Type, Authorization
Credentials support: Enabled

### Production CORS Configuration

**CRITICAL SECURITY NOTE**: The current CORS configuration is for development only. Before deploying to production:

1. Update the allowed origins in `app/__init__.py` to match your production frontend URL
2. Never use wildcard origins (`*`) in production
3. Restrict origins to only your trusted frontend domains

Example production configuration:
```python
CORS(app, 
     origins=['https://your-production-frontend.com'],
     methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)
```

---

## Development

### Adding New Endpoints

1. Add route handler in `app/routes/workshop_routes.py`
2. Add business logic in appropriate service file
3. Add data access methods in `app/store/workshop_store.py` if needed
4. Add validation in `app/validators.py` if needed
5. Write tests in `tests/unit/` and `tests/property/`

### Code Style

The project follows Python best practices:
- PEP 8 style guide
- Type hints where appropriate
- Docstrings for functions and classes
- Descriptive variable and function names

### Running in Production

For production deployment, use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3535 app:app
```

**Production Considerations:**
- Use environment variables for configuration
- Implement proper logging
- Add authentication/authorization
- Use a proper database instead of JSON file
- Set up monitoring and error tracking
- Enable HTTPS
- Configure CORS properly

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

## License

This project is provided as-is for educational purposes.

---

## Support

For issues, questions, or suggestions:
- Check the Troubleshooting section above
- Review the test files for usage examples
- Examine the verification report: `verification_report.md`

---

## Acknowledgments

Built with:
- Flask - Web framework
- pytest - Testing framework
- hypothesis - Property-based testing library
