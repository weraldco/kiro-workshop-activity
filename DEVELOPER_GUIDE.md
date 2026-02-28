# Developer Guide

Complete guide for developers working on the Workshop Management System.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Architecture](#architecture)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Database](#database)
7. [API Development](#api-development)
8. [Frontend Development](#frontend-development)
9. [Debugging](#debugging)
10. [Contributing](#contributing)

---

## Development Setup

### Prerequisites

- Python 3.8+ with pip
- Node.js 14+ with npm
- MySQL 8.0+
- Git
- Code editor (VS Code recommended)

### Initial Setup

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/workshop-management.git
cd workshop-management
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python init_db.py
```

3. **Frontend Setup**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

4. **Database Setup**
```bash
mysql -u root -p < backend/schema.sql
```

### Running Development Servers

**Backend** (Terminal 1):
```bash
cd backend
source venv/bin/activate
python run.py
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

### Development Tools

**Recommended VS Code Extensions**:
- Python
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitLens

**Recommended Browser Extensions**:
- React Developer Tools
- Redux DevTools (if using Redux)

---

## Project Structure

```
workshop-management/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── auth/                # Authentication module
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py  # JWT token management
│   │   │   ├── password_service.py  # Password hashing
│   │   │   └── decorators.py    # Auth decorators
│   │   ├── database/            # Database module
│   │   │   ├── __init__.py
│   │   │   └── connection.py    # MySQL connection
│   │   ├── routes/              # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── workshop_routes_v2.py
│   │   │   └── participant_routes.py
│   │   ├── store/               # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── user_store.py
│   │   │   ├── workshop_store_mysql.py
│   │   │   └── participant_store.py
│   │   └── validators.py        # Input validation
│   ├── tests/                   # Backend tests
│   │   ├── test_auth_services.py
│   │   ├── test_auth_endpoints.py
│   │   ├── test_user_store.py
│   │   ├── test_validators_auth.py
│   │   ├── test_workshop_endpoints.py
│   │   ├── test_participant_endpoints.py
│   │   └── test_integration_workflow.py
│   ├── .env                     # Environment variables
│   ├── .env.example             # Environment template
│   ├── init_db.py               # Database initialization
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Application entry point
│
├── frontend/
│   ├── components/              # React components
│   │   ├── auth/                # Auth components
│   │   │   ├── SignInForm.tsx
│   │   │   ├── SignUpForm.tsx
│   │   │   └── __tests__/
│   │   ├── dashboard/           # Dashboard components
│   │   │   ├── CreateWorkshopModal.tsx
│   │   │   ├── JoinedWorkshopCard.tsx
│   │   │   ├── MyWorkshopCard.tsx
│   │   │   └── __tests__/
│   │   ├── layout/              # Layout components
│   │   │   └── DashboardLayout.tsx
│   │   ├── workshop/            # Workshop components
│   │   │   ├── JoinButton.tsx
│   │   │   ├── ParticipantList.tsx
│   │   │   ├── PendingRequestCard.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   ├── WorkshopCard.tsx
│   │   │   └── __tests__/
│   │   └── ProtectedRoute.tsx   # Route protection
│   ├── contexts/                # React contexts
│   │   └── AuthContext.tsx      # Auth state management
│   ├── lib/                     # Utility functions
│   │   ├── auth.ts              # Auth API calls
│   │   ├── storage.ts           # Local storage utils
│   │   └── workshops.ts         # Workshop API calls
│   ├── pages/                   # Next.js pages
│   │   ├── auth/
│   │   │   ├── signin.tsx
│   │   │   └── signup.tsx
│   │   ├── dashboard/
│   │   │   ├── index.tsx
│   │   │   └── workshops/[id].tsx
│   │   ├── workshops/
│   │   │   ├── index.tsx
│   │   │   └── [id].tsx
│   │   ├── _app.tsx             # App wrapper
│   │   └── index.tsx            # Home page
│   ├── styles/                  # Global styles
│   ├── types/                   # TypeScript types
│   │   ├── auth.ts
│   │   └── workshop.ts
│   ├── .env.local               # Environment variables
│   ├── .env.local.example       # Environment template
│   ├── jest.config.js           # Jest configuration
│   ├── jest.setup.js            # Jest setup
│   ├── next.config.js           # Next.js configuration
│   ├── package.json             # Node dependencies
│   ├── tailwind.config.js       # Tailwind configuration
│   └── tsconfig.json            # TypeScript configuration
│
└── docs/                        # Documentation
    ├── README.md
    ├── API_DOCUMENTATION.md
    ├── USER_GUIDE.md
    ├── DEVELOPER_GUIDE.md
    └── DEPLOYMENT.md
```

---

## Architecture

### Backend Architecture

**Layered Architecture**:
```
Routes (API Layer)
    ↓
Services (Business Logic)
    ↓
Store (Data Access Layer)
    ↓
Database (MySQL)
```

**Key Components**:

1. **Routes**: Handle HTTP requests/responses
2. **Services**: Business logic and validation
3. **Store**: Database operations
4. **Auth**: Authentication and authorization
5. **Validators**: Input validation

### Frontend Architecture

**Component-Based Architecture**:
```
Pages (Next.js Routes)
    ↓
Layout Components
    ↓
Feature Components
    ↓
UI Components
```

**State Management**:
- React Context for auth state
- Component state for UI state
- No global state management (Redux not needed)

**Data Flow**:
```
User Action → Component → API Call → Backend → Database
                ↓
            Update State
                ↓
            Re-render UI
```

---

## Coding Standards

### Python (Backend)

**Style Guide**: PEP 8

**Naming Conventions**:
```python
# Functions and variables: snake_case
def get_user_by_id(user_id):
    user_name = "John"

# Classes: PascalCase
class UserStore:
    pass

# Constants: UPPER_SNAKE_CASE
JWT_SECRET_KEY = "secret"

# Private methods: _leading_underscore
def _internal_method():
    pass
```

**Docstrings**:
```python
def create_workshop(title, description, owner_id):
    """
    Create a new workshop.
    
    Args:
        title (str): Workshop title
        description (str): Workshop description
        owner_id (str): Owner user ID
    
    Returns:
        dict: Created workshop data
    
    Raises:
        ValueError: If validation fails
    """
    pass
```

**Imports**:
```python
# Standard library
import os
import uuid

# Third-party
from flask import Flask, request
import mysql.connector

# Local
from app.auth import auth_service
from app.store import user_store
```

### TypeScript (Frontend)

**Style Guide**: Airbnb TypeScript Style Guide

**Naming Conventions**:
```typescript
// Variables and functions: camelCase
const userName = "John";
function getUserById(userId: string) {}

// Interfaces and Types: PascalCase
interface User {
  id: string;
  name: string;
}

// Components: PascalCase
const UserCard: React.FC<Props> = () => {};

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = "http://localhost:3535";
```

**Type Annotations**:
```typescript
// Always use explicit types
const user: User = { id: "123", name: "John" };

// Function parameters and return types
function getUser(id: string): Promise<User> {
  return fetch(`/api/users/${id}`).then(r => r.json());
}

// Component props
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}
```

**Component Structure**:
```typescript
/**
 * Component description
 */
import React from 'react';

interface ComponentProps {
  // Props definition
}

const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks
  const [state, setState] = useState();
  
  // Event handlers
  const handleClick = () => {};
  
  // Effects
  useEffect(() => {}, []);
  
  // Render
  return <div>...</div>;
};

export default Component;
```

---

## Testing

### Backend Testing

**Test Structure**:
```python
def test_feature_name():
    """Test description"""
    # Arrange
    data = {...}
    
    # Act
    result = function(data)
    
    # Assert
    assert result == expected
```

**Running Tests**:
```bash
# All tests
pytest

# Specific file
pytest tests/test_auth_endpoints.py

# Specific test
pytest tests/test_auth_endpoints.py::test_register_success

# With coverage
pytest --cov=app --cov-report=html

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

**Writing Tests**:
```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_create_workshop(client):
    # Register and login
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'name': 'Test User'
    })
    token = response.get_json()['access_token']
    
    # Create workshop
    response = client.post('/api/workshops',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Workshop',
            'description': 'Test description'
        }
    )
    
    assert response.status_code == 201
    assert response.get_json()['title'] == 'Test Workshop'
```

### Frontend Testing

**Test Structure**:
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

describe('Component', () => {
  it('should do something', async () => {
    // Arrange
    render(<Component />);
    
    // Act
    fireEvent.click(screen.getByRole('button'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Expected')).toBeInTheDocument();
    });
  });
});
```

**Running Tests**:
```bash
# All tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm test -- --coverage

# Specific file
npm test -- SignUpForm.test.tsx
```

**Writing Tests**:
```typescript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SignUpForm from '../SignUpForm';

// Mock dependencies
jest.mock('../../../lib/auth');

describe('SignUpForm', () => {
  it('renders form fields', () => {
    render(<SignUpForm />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });
  
  it('submits form with valid data', async () => {
    render(<SignUpForm />);
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'Test123!@#' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));
    
    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalled();
    });
  });
});
```

---

## Database

### Schema

See `backend/init_db.py` for complete schema.

**Key Tables**:

```sql
-- Users
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workshops
CREATE TABLE workshops (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('pending', 'ongoing', 'completed') DEFAULT 'pending',
    signup_enabled BOOLEAN DEFAULT TRUE,
    owner_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Participants
CREATE TABLE participants (
    id VARCHAR(36) PRIMARY KEY,
    workshop_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    status ENUM('pending', 'joined', 'rejected', 'waitlisted') DEFAULT 'pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP NULL,
    approved_by VARCHAR(36) NULL,
    UNIQUE KEY unique_participation (workshop_id, user_id),
    FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
);
```

### Migrations

Currently using manual migrations. For future:

1. Create migration file: `migrations/001_add_column.sql`
2. Apply migration: `mysql < migrations/001_add_column.sql`
3. Track in migrations table

**Recommended**: Use Alembic for Python migrations.

### Database Access

**Connection Management**:
```python
from app.database.connection import get_db_connection

# Get connection
conn = get_db_connection()
try:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
finally:
    cursor.close()
    conn.close()
```

**Best Practices**:
- Always use parameterized queries
- Close connections in finally blocks
- Use transactions for multiple operations
- Handle connection errors gracefully

---

## API Development

### Adding a New Endpoint

1. **Define Route**:
```python
# backend/app/routes/feature_routes.py
from flask import Blueprint, request, jsonify
from app.auth.decorators import require_auth

feature_bp = Blueprint('feature', __name__, url_prefix='/api')

@feature_bp.route('/features', methods=['POST'])
@require_auth
def create_feature():
    """Create a new feature"""
    data = request.get_json(silent=True)
    
    # Validate
    if not data or not data.get('name'):
        return jsonify({
            "error": "Name is required",
            "code": "VALIDATION_ERROR",
            "status": 400
        }), 400
    
    # Process
    feature = feature_store.create(data)
    
    return jsonify(feature), 201
```

2. **Register Blueprint**:
```python
# backend/app/__init__.py
from app.routes.feature_routes import feature_bp

app.register_blueprint(feature_bp)
```

3. **Add Tests**:
```python
# backend/tests/test_feature_endpoints.py
def test_create_feature(client, auth_token):
    response = client.post('/api/features',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Test Feature'}
    )
    assert response.status_code == 201
```

4. **Document**:
Add to `API_DOCUMENTATION.md`

### Error Handling

**Standard Error Response**:
```python
return jsonify({
    "error": "Error message",
    "code": "ERROR_CODE",
    "status": 400
}), 400
```

**Error Codes**:
- `VALIDATION_ERROR`: Input validation failed
- `UNAUTHORIZED`: Authentication required
- `FORBIDDEN`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `SERVER_ERROR`: Internal error

---

## Frontend Development

### Adding a New Page

1. **Create Page**:
```typescript
// frontend/pages/features/index.tsx
import React from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';

const FeaturesPage: React.FC = () => {
  return (
    <ProtectedRoute>
      <div>
        <h1>Features</h1>
      </div>
    </ProtectedRoute>
  );
};

export default FeaturesPage;
```

2. **Add Navigation**:
```typescript
// Update navigation in DashboardLayout.tsx
const navigation = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Features', href: '/features' },
];
```

### Adding a New Component

1. **Create Component**:
```typescript
// frontend/components/features/FeatureCard.tsx
import React from 'react';

interface FeatureCardProps {
  feature: Feature;
  onDelete?: (id: string) => void;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ feature, onDelete }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-semibold">{feature.name}</h3>
      {onDelete && (
        <button onClick={() => onDelete(feature.id)}>
          Delete
        </button>
      )}
    </div>
  );
};

export default FeatureCard;
```

2. **Add Tests**:
```typescript
// frontend/components/features/__tests__/FeatureCard.test.tsx
import { render, screen } from '@testing-library/react';
import FeatureCard from '../FeatureCard';

describe('FeatureCard', () => {
  it('renders feature name', () => {
    const feature = { id: '1', name: 'Test Feature' };
    render(<FeatureCard feature={feature} />);
    expect(screen.getByText('Test Feature')).toBeInTheDocument();
  });
});
```

### API Integration

**Create API Service**:
```typescript
// frontend/lib/features.ts
import { authApi } from './auth';

export const getFeatures = async () => {
  const response = await authApi.get('/api/features');
  return response.data;
};

export const createFeature = async (data: CreateFeatureData) => {
  const response = await authApi.post('/api/features', data);
  return response.data;
};
```

**Use in Component**:
```typescript
const [features, setFeatures] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  const fetchFeatures = async () => {
    try {
      const data = await getFeatures();
      setFeatures(data);
    } catch (error) {
      console.error('Failed to fetch features', error);
    } finally {
      setLoading(false);
    }
  };
  
  fetchFeatures();
}, []);
```

---

## Debugging

### Backend Debugging

**Print Debugging**:
```python
print(f"Debug: user_id={user_id}, data={data}")
```

**Logging**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing request: {data}")
logger.error(f"Error occurred: {str(e)}")
```

**VS Code Debugger**:
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "run.py",
        "FLASK_ENV": "development"
      },
      "args": ["run", "--no-debugger", "--no-reload"],
      "jinja": true
    }
  ]
}
```

### Frontend Debugging

**Console Logging**:
```typescript
console.log('Debug:', data);
console.error('Error:', error);
console.table(users);
```

**React DevTools**:
- Install React Developer Tools extension
- Inspect component props and state
- View component hierarchy

**Network Tab**:
- Open browser DevTools (F12)
- Go to Network tab
- Monitor API requests/responses
- Check request headers and payloads

**VS Code Debugger**:
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    }
  ]
}
```

---

## Contributing

### Git Workflow

1. **Create Branch**:
```bash
git checkout -b feature/new-feature
```

2. **Make Changes**:
```bash
# Edit files
git add .
git commit -m "Add new feature"
```

3. **Push Branch**:
```bash
git push origin feature/new-feature
```

4. **Create Pull Request**:
- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Add description
- Request review

### Commit Messages

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat(auth): add password reset functionality

Implement password reset via email with token expiration.

Closes #123
```

```
fix(workshop): prevent duplicate join requests

Add unique constraint check before creating participant.

Fixes #456
```

### Code Review

**Checklist**:
- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log statements
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Performance optimized

### Release Process

1. Update version in `package.json` and `__init__.py`
2. Update CHANGELOG.md
3. Create release branch
4. Run all tests
5. Create release tag
6. Deploy to production
7. Monitor for issues

---

## Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [MySQL Workbench](https://www.mysql.com/products/workbench/) - Database management
- [VS Code](https://code.visualstudio.com/) - Code editor

### Learning
- [Python Best Practices](https://docs.python-guide.org/)
- [React Patterns](https://reactpatterns.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

---

**Questions?** Check the [API Documentation](API_DOCUMENTATION.md) or create an issue on GitHub.
