# Quick Start Guide

## Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL 8.0+

## Setup (5 minutes)

### 1. Database Setup

```bash
# Create MySQL database and user
mysql -u root -p

CREATE DATABASE workshop_management;
CREATE USER 'workshop_user'@'localhost' IDENTIFIED BY 'password1';
GRANT ALL PRIVILEGES ON workshop_management.* TO 'workshop_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_EXPIRATION_MINUTES=30
DB_HOST=localhost
DB_PORT=3306
DB_NAME=workshop_management
DB_USER=workshop_user
DB_PASSWORD=password1
EOF

# Initialize database
python init_db.py

# Run tests (optional)
pytest

# Start server
python run.py
```

Backend will run on http://localhost:3535

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:3535
EOF

# Start development server
npm run dev
```

Frontend will run on http://localhost:3000

## Test the Application

### 1. Register a User
- Visit http://localhost:3000/auth/signup
- Enter name, email, password
- Click "Sign up"

### 2. Create a Workshop
- You'll be redirected to dashboard
- Click "Create Workshop"
- Enter title and description
- Click "Create Workshop"

### 3. Join a Workshop (with second user)
- Open incognito window
- Register another user
- Visit http://localhost:3000/workshops
- Click "Join" on a workshop
- Request will be pending

### 4. Approve Join Request
- Switch back to first user
- Click "Manage" on your workshop
- See pending request
- Click "Approve"

### 5. Verify Participant Joined
- Participant appears in "Participants" section
- Second user sees workshop in "Joined Workshops"

## Common Issues

### Backend won't start
- Check MySQL is running: `mysql -u workshop_user -p`
- Verify database exists: `SHOW DATABASES;`
- Check .env file has correct credentials

### Frontend can't connect to backend
- Verify backend is running on port 3535
- Check .env.local has correct API URL
- Check browser console for CORS errors

### Tests failing
- Ensure test database is clean: `python init_db.py`
- Check all dependencies installed: `pip install -r requirements.txt`

## Default Ports

- Backend: 3535
- Frontend: 3000
- MySQL: 3306

## API Testing with curl

### Register User
```bash
curl -X POST http://localhost:3535/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#",
    "name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:3535/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#"
  }'
```

### Create Workshop (replace TOKEN)
```bash
curl -X POST http://localhost:3535/api/workshops \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "My Workshop",
    "description": "Workshop description"
  }'
```

## Next Steps

1. Read `PROJECT_COMPLETE.md` for full feature list
2. Check `IMPLEMENTATION_CHECKLIST.md` for development details
3. Review API endpoints in backend route files
4. Explore the codebase and customize as needed

## Production Deployment

Before deploying to production:

1. Change JWT_SECRET_KEY to a strong random value
2. Use production database credentials
3. Enable HTTPS
4. Update CORS origins
5. Set up proper logging
6. Configure rate limiting
7. Set up monitoring and backups

See `PROJECT_COMPLETE.md` for full deployment checklist.

## Support

For issues or questions:
1. Check the documentation files
2. Review the code comments
3. Check the test files for usage examples
4. Review the API endpoint documentation in route files

Happy coding! 🚀
