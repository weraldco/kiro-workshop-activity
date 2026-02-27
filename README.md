# Workshop Management System

A full-stack TypeScript application for managing workshops with lifecycle states (pending, ongoing, completed), participant signups, and challenge visibility control. Built with Node.js backend API and Next.js frontend.

## Features

- 🎯 Workshop lifecycle management (pending → ongoing → completed)
- 👥 State-driven participant signup control
- 📝 Challenge visibility based on workshop status
- 🔐 Access control for participants and challenges
- 💾 JSON file-based persistence
- ✅ Comprehensive validation and referential integrity
- 🔄 RESTful API design with TypeScript
- 🎨 Next.js frontend with TailwindCSS
- 🧪 174 automated tests (all passing)

## Requirements

- Node.js 16.x or higher
- npm or yarn package manager

## Quick Start

### 1. Installation

Clone the repository and navigate to the project directory:

```bash
cd workshop-management-system
```

Install backend dependencies:

```bash
cd backend
npm install
```

Install frontend dependencies:

```bash
cd ../frontend
npm install
```

### 2. Running the Application

#### Backend API

Start the backend server:

```bash
cd backend
npm run dev
```

The API will be available at `http://localhost:3535`

#### Frontend

In a separate terminal, start the frontend development server:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Test the API

Open a new terminal and try creating a workshop:

```bash
curl -X POST http://localhost:3535/api/workshops \
  -H "Content-Type: application/json" \
  -d '{
    "title": "TypeScript Workshop",
    "description": "Learn TypeScript fundamentals"
  }'
```

You should receive a `201 Created` response with the workshop details.

## API Endpoints

All API endpoints are prefixed with `/api` and return JSON responses.

### Response Format

**Success Response:**
```json
{
  "id": "uuid",
  "title": "Workshop Title",
  "status": "pending",
  ...
}
```

**Error Response:**
```json
{
  "error": "Human-readable error description",
  "code": "ERROR_CODE",
  "status": 400
}
```

---

### Workshop Endpoints

#### 1. Create Workshop

Creates a new workshop with default status='pending' and signup_enabled=true.

**Endpoint:** `POST /api/workshops`

**Request Body:**
```json
{
  "title": "TypeScript Workshop",
  "description": "Learn TypeScript fundamentals"
}
```

**Field Descriptions:**
- `title` (string, required): Workshop title (1-200 characters)
- `description` (string, required): Workshop description (1-1000 characters)

**Success Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "TypeScript Workshop",
  "description": "Learn TypeScript fundamentals",
  "status": "pending",
  "signup_enabled": true,
  "created_at": "2026-02-27T00:00:00.000Z",
  "updated_at": "2026-02-27T00:00:00.000Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (missing title/description, length violations)
- `500 Internal Server Error`: Database error

---

#### 2. List All Workshops

Retrieves all workshops in the system.

**Endpoint:** `GET /api/workshops`

**Success Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "TypeScript Workshop",
    "description": "Learn TypeScript fundamentals",
    "status": "pending",
    "signup_enabled": true,
    "created_at": "2026-02-27T00:00:00.000Z",
    "updated_at": "2026-02-27T00:00:00.000Z"
  }
]
```

---

#### 3. Update Workshop Status

Updates the workshop status (pending → ongoing → completed).

**Endpoint:** `PATCH /api/workshops/:id/status`

**Request Body:**
```json
{
  "status": "ongoing"
}
```

**Valid Status Values:**
- `pending`: Workshop is open for signups
- `ongoing`: Workshop is in progress, challenges visible to participants
- `completed`: Workshop is finished

**Success Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "TypeScript Workshop",
  "status": "ongoing",
  "updated_at": "2026-02-27T01:00:00.000Z",
  ...
}
```

**Error Responses:**
- `400 Bad Request`: Invalid status value
- `404 Not Found`: Workshop not found

---

#### 4. Toggle Signup Flag

Enables or disables participant signups for a workshop.

**Endpoint:** `PATCH /api/workshops/:id/signup-flag`

**Request Body:**
```json
{
  "signup_enabled": false
}
```

**Success Response:** `200 OK`

**Error Responses:**
- `400 Bad Request`: Invalid boolean value
- `404 Not Found`: Workshop not found

---

### Participant Endpoints

#### 5. Sign Up for Workshop

Registers a participant for a workshop (only allowed when status='pending' AND signup_enabled=true).

**Endpoint:** `POST /api/workshops/:id/signup`

**Request Body:**
```json
{
  "user_id": "user123"
}
```

**Success Response:** `201 Created`
```json
{
  "success": true,
  "participant_id": "660e8400-e29b-41d4-a716-446655440001"
}
```

**Error Responses:**
- `400 Bad Request`: Missing user_id
- `403 Forbidden`: Signups not allowed (status not pending or signup_enabled=false)
- `404 Not Found`: Workshop not found
- `409 Conflict`: Duplicate signup

---

#### 6. List Workshop Participants

Retrieves all participants for a specific workshop.

**Endpoint:** `GET /api/workshops/:id/participants`

**Success Response:** `200 OK`
```json
{
  "participants": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "user123",
      "signed_up_at": "2026-02-27T00:30:00.000Z"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: Workshop not found

---

### Challenge Endpoints

#### 7. Create Challenge

Creates a new challenge for a workshop.

**Endpoint:** `POST /api/workshops/:id/challenges`

**Request Body:**
```json
{
  "title": "Build a REST API",
  "description": "Create a RESTful API with TypeScript",
  "html_content": "<h1>Challenge Instructions</h1><p>Build an API...</p>"
}
```

**Field Descriptions:**
- `title` (string, required): Challenge title (1-200 characters)
- `description` (string, required): Challenge description (1-1000 characters)
- `html_content` (string, required): HTML content for the challenge

**Success Response:** `201 Created`
```json
{
  "success": true,
  "challenge_id": "770e8400-e29b-41d4-a716-446655440002"
}
```

**Error Responses:**
- `400 Bad Request`: Validation error (missing fields, length violations, invalid HTML)
- `404 Not Found`: Workshop not found

---

#### 8. List Workshop Challenges

Retrieves challenges for a workshop (only accessible when status='ongoing' AND user is a participant).

**Endpoint:** `GET /api/workshops/:id/challenges?user_id=user123`

**Query Parameters:**
- `user_id` (string, required): User requesting access

**Success Response:** `200 OK`
```json
{
  "challenges": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Build a REST API",
      "description": "Create a RESTful API with TypeScript",
      "html_content": "<h1>Challenge Instructions</h1>..."
    }
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Missing user_id
- `403 Forbidden`: Access denied (workshop not ongoing or user not a participant)
- `404 Not Found`: Workshop not found

---

#### 9. Get Challenge Details

Retrieves a specific challenge (with access control).

**Endpoint:** `GET /api/challenges/:id?user_id=user123`

**Query Parameters:**
- `user_id` (string, required): User requesting access

**Success Response:** `200 OK`
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "workshop_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Build a REST API",
  "description": "Create a RESTful API with TypeScript",
  "html_content": "<h1>Challenge Instructions</h1>..."
}
```

**Error Responses:**
- `400 Bad Request`: Missing user_id
- `403 Forbidden`: Access denied
- `404 Not Found`: Challenge not found

---

## Complete API Workflow Example

Here's a complete workflow demonstrating the workshop lifecycle:

```bash
# 1. Create a workshop
WORKSHOP_RESPONSE=$(curl -s -X POST http://localhost:3535/api/workshops \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced TypeScript",
    "description": "Deep dive into TypeScript advanced features"
  }')

# Extract workshop ID (requires jq)
WORKSHOP_ID=$(echo $WORKSHOP_RESPONSE | jq -r '.id')
echo "Created workshop: $WORKSHOP_ID"

# 2. List all workshops
curl http://localhost:3535/api/workshops

# 3. Sign up participants (workshop is in 'pending' status)
curl -X POST http://localhost:3535/api/workshops/$WORKSHOP_ID/signup \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice123"}'

curl -X POST http://localhost:3535/api/workshops/$WORKSHOP_ID/signup \
  -H "Content-Type: application/json" \
  -d '{"user_id": "bob456"}'

# 4. Create challenges
curl -X POST http://localhost:3535/api/workshops/$WORKSHOP_ID/challenges \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Type Guards Challenge",
    "description": "Implement custom type guards",
    "html_content": "<h1>Challenge</h1><p>Create type guards...</p>"
  }'

# 5. Start the workshop (change status to 'ongoing')
curl -X PATCH http://localhost:3535/api/workshops/$WORKSHOP_ID/status \
  -H "Content-Type: application/json" \
  -d '{"status": "ongoing"}'

# 6. Participants can now access challenges
curl "http://localhost:3535/api/workshops/$WORKSHOP_ID/challenges?user_id=alice123"

# 7. Complete the workshop
curl -X PATCH http://localhost:3535/api/workshops/$WORKSHOP_ID/status \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

## Access Control Rules

The system enforces strict access control based on workshop status:

### Signup Rules
- ✅ Allowed: `status='pending'` AND `signup_enabled=true`
- ❌ Blocked: `status='ongoing'` OR `status='completed'` OR `signup_enabled=false`

### Challenge Visibility Rules
- ✅ Visible: `status='ongoing'` AND user is a participant
- ❌ Hidden: `status='pending'` OR `status='completed'` OR user is not a participant

### Status Transitions
```
pending → ongoing → completed
```

---

## Data Models

### Workshop
```typescript
interface Workshop {
  id: string;                    // UUID v4
  title: string;                 // 1-200 characters
  description: string;           // 1-1000 characters
  status: 'pending' | 'ongoing' | 'completed';
  signup_enabled: boolean;       // Default: true
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
}
```

### Participant
```typescript
interface Participant {
  id: string;                    // UUID v4
  workshop_id: string;           // Foreign key to Workshop
  user_id: string;               // User identifier
  signed_up_at: string;          // ISO 8601 timestamp
}
```

### Challenge
```typescript
interface Challenge {
  id: string;                    // UUID v4
  workshop_id: string;           // Foreign key to Workshop
  title: string;                 // 1-200 characters
  description: string;           // 1-1000 characters
  html_content: string;          // Valid HTML
}
```

---

## HTTP Status Codes

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| `200 OK` | Success | GET/PATCH requests return data successfully |
| `201 Created` | Resource created | POST requests create new resources successfully |
| `400 Bad Request` | Invalid input | Validation fails (missing fields, length violations, invalid values) |
| `403 Forbidden` | Access denied | Signup not allowed, challenge access denied |
| `404 Not Found` | Resource not found | Workshop/Challenge/Participant ID does not exist |
| `409 Conflict` | Duplicate resource | Duplicate participant signup |
| `500 Internal Server Error` | Server error | Database errors, unexpected server errors |

---

## Data Persistence

### Storage Location

Data is persisted to JSON files in the `backend/src/database/` directory:
- `workshops.json` - Workshop records
- `participants.json` - Participant records
- `challenges.json` - Challenge records

### File Structure

**workshops.json:**
```json
[
  {
    "id": "uuid-v4",
    "title": "Workshop Title",
    "description": "Workshop Description",
    "status": "pending",
    "signup_enabled": true,
    "created_at": "2026-02-27T00:00:00.000Z",
    "updated_at": "2026-02-27T00:00:00.000Z"
  }
]
```

**participants.json:**
```json
[
  {
    "id": "uuid-v4",
    "workshop_id": "uuid-v4",
    "user_id": "user123",
    "signed_up_at": "2026-02-27T00:00:00.000Z"
  }
]
```

**challenges.json:**
```json
[
  {
    "id": "uuid-v4",
    "workshop_id": "uuid-v4",
    "title": "Challenge Title",
    "description": "Challenge Description",
    "html_content": "<h1>Content</h1>"
  }
]
```

### Atomic Write Operations

All write operations use atomic file operations:
1. Write to temporary file (`.tmp` extension)
2. Rename temporary file to target file (atomic operation)
3. Ensures data consistency even during concurrent writes

### Referential Integrity

The system maintains referential integrity:
- Participants must reference existing workshops
- Challenges must reference existing workshops
- Validation occurs before write operations

---

## Testing

### Backend Tests

Run all backend tests:

```bash
cd backend
npm test
```

**Test Results (as of latest run):**
- Total: 148 tests
- Passing: 148 tests ✅
- Failing: 0 tests

**Test Coverage:**
- Unit tests: Database service, validation, access control, referential integrity
- Controller tests: Workshop, participant, and challenge controllers
- Integration tests: End-to-end API workflows

### Frontend Tests

Run all frontend tests:

```bash
cd frontend
npm test
```

**Test Results:**
- Total: 26 tests
- Passing: 26 tests ✅

**Test Coverage:**
- Component tests: WorkshopCard, WorkshopList
- Rendering tests: Workshop display, error handling, loading states

### Known Issues

~~All tests are now passing!~~ No known issues at this time.

### Run Tests with Coverage

```bash
cd backend
npm test -- --coverage
```

### Run Specific Test Suites

```bash
# Unit tests only
npm test -- src/services/

# Controller tests only
npm test -- src/controllers/

# Integration tests only
npm test -- src/integration.test.ts src/e2e.test.ts
```

---

## Troubleshooting

### Port Already in Use

**Problem:** Error message: "Port 3535 is already in use"

**Solution 1:** Change the port in `backend/src/server.ts`:
```typescript
const PORT = process.env.PORT || 5002;  // Use different port
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

**Problem:** `Cannot find module` errors

**Solution:** Make sure you've installed dependencies:
```bash
cd backend
npm install

cd ../frontend
npm install
```

### TypeScript Compilation Errors

**Problem:** TypeScript errors when running the application

**Solution:** Check TypeScript configuration and rebuild:
```bash
cd backend
npm run build
```

### Database File Permission Error

**Problem:** Cannot read/write JSON database files

**Solution:** Check file permissions:
```bash
chmod 644 backend/src/database/*.json
```

### Connection Refused

**Problem:** `ECONNREFUSED` when accessing API

**Solution:** Make sure the backend server is running:
```bash
cd backend
npm run dev
```

Check the terminal for any error messages.

### Frontend Not Loading

**Problem:** Frontend shows blank page or errors

**Solution:**
1. Check if backend is running on port 3535
2. Check browser console for errors
3. Verify API URL in frontend configuration
4. Clear browser cache and reload

### Tests Failing

**Problem:** Some tests fail when running `npm test`

**Solution:**
1. Make sure all dependencies are installed: `npm install`
2. Check if database files are locked by another process
3. Delete test artifacts: `rm -rf node_modules/.cache`
4. Run tests again: `npm test`

**Known Issues:** See the "Known Issues" section under Testing for expected test failures.

### CORS Errors

**Problem:** Browser shows CORS policy errors

**Solution:** The backend is configured with CORS enabled. If you're still seeing errors:
1. Check that backend is running on port 3535
2. Verify frontend is making requests to correct URL
3. Check browser console for specific CORS error details

---

## Project Structure

```
workshop-management-system/
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   │   ├── workshop.controller.ts
│   │   │   ├── workshop.controller.test.ts
│   │   │   ├── participant.controller.ts
│   │   │   ├── participant.controller.test.ts
│   │   │   ├── participant.integration.test.ts
│   │   │   ├── challenge.controller.ts
│   │   │   └── challenge.controller.test.ts
│   │   ├── services/
│   │   │   ├── database.service.ts
│   │   │   ├── database.service.test.ts
│   │   │   ├── validation.service.ts
│   │   │   ├── validation.service.test.ts
│   │   │   ├── access-control.service.ts
│   │   │   ├── access-control.service.test.ts
│   │   │   ├── referential-integrity.service.ts
│   │   │   └── referential-integrity.service.test.ts
│   │   ├── routes/
│   │   │   └── workshop.routes.ts
│   │   ├── database/
│   │   │   ├── workshops.json
│   │   │   ├── participants.json
│   │   │   └── challenges.json
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── app.ts
│   │   ├── server.ts
│   │   ├── integration.test.ts
│   │   └── e2e.test.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── jest.config.js
├── frontend/
│   ├── pages/
│   │   └── index.tsx
│   ├── components/
│   │   ├── WorkshopCard.tsx
│   │   ├── WorkshopCard.test.tsx
│   │   ├── WorkshopList.tsx
│   │   └── WorkshopList.test.tsx
│   ├── lib/
│   │   └── api.ts
│   ├── styles/
│   │   └── globals.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
├── .kiro/
│   └── specs/
│       └── workshop-management-system/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── README.md
└── .gitignore
```

---

## Architecture

The application follows a layered architecture with clear separation of concerns:

### Backend Architecture

**1. API Layer (Controllers)**
- Handles HTTP requests and responses
- Request validation and parsing
- Response formatting
- Error handling

**2. Business Logic Layer (Services)**
- **Database Service**: JSON file read/write operations
- **Validation Service**: Schema validation for all entities
- **Access Control Service**: Authorization logic for signups and challenges
- **Referential Integrity Service**: Maintains relationships between entities

**3. Data Layer**
- JSON file-based persistence
- Atomic write operations
- Schema enforcement

### Frontend Architecture

**1. Pages**
- Next.js page components
- Server-side rendering support
- Routing

**2. Components**
- **WorkshopCard**: Displays individual workshop information
- **WorkshopList**: Fetches and displays all workshops
- Reusable UI components

**3. API Client**
- HTTP communication with backend
- Error handling
- Response parsing

### Design Principles

- **Separation of Concerns**: Each layer has a single responsibility
- **Type Safety**: TypeScript throughout the stack
- **Testability**: Each component is independently testable
- **Maintainability**: Clear structure and naming conventions
- **Scalability**: Easy to extend with new features

---

## Development

### Adding New Endpoints

1. Add route handler in `backend/src/routes/workshop.routes.ts`
2. Add controller method in appropriate controller file
3. Add business logic in service files if needed
4. Add validation in `ValidationService` if needed
5. Write tests in corresponding `.test.ts` files

### Code Style

The project follows TypeScript best practices:
- ESLint for code linting
- Prettier for code formatting
- Type safety throughout
- Descriptive variable and function names
- JSDoc comments for public APIs

### Running in Development

Backend with hot reload:
```bash
cd backend
npm run dev
```

Frontend with hot reload:
```bash
cd frontend
npm run dev
```

### Building for Production

Backend:
```bash
cd backend
npm run build
npm start
```

Frontend:
```bash
cd frontend
npm run build
npm start
```

### Production Considerations

- Use environment variables for configuration
- Implement proper logging (Winston, Pino)
- Add authentication/authorization (JWT, OAuth)
- Use a proper database (PostgreSQL, MongoDB)
- Set up monitoring and error tracking (Sentry, DataDog)
- Enable HTTPS
- Configure CORS properly for production domains
- Implement rate limiting
- Add input sanitization
- Set up CI/CD pipeline

---

## Specification-Driven Development

This project was built using a specification-driven development approach. The complete specification is available in `.kiro/specs/workshop-management-system/`:

- **requirements.md**: Business requirements and acceptance criteria
- **design.md**: Technical design, architecture, and correctness properties
- **tasks.md**: Implementation plan with incremental tasks

This approach ensures:
- Clear requirements before implementation
- Traceability from requirements to code
- Systematic testing strategy
- Incremental development with validation checkpoints

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass (or document known failures)
5. Follow the existing code style
6. Submit a pull request with clear description

---

## License

This project is provided as-is for educational purposes.

---

## Support

For issues, questions, or suggestions:
- Check the Troubleshooting section above
- Review the specification files in `.kiro/specs/workshop-management-system/`
- Check the test files for usage examples
- Review the Known Issues section for current limitations

---

## Acknowledgments

Built with:
- **Backend**: Node.js, TypeScript, Express, Jest
- **Frontend**: Next.js, React, TailwindCSS, TypeScript
- **Testing**: Jest, React Testing Library
- **Development**: Specification-driven development methodology
