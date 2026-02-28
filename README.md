# Workshop Management System

A full-stack web application for creating, managing, and joining workshops with authentication and participant approval workflows.

## Features

- 🔐 **User Authentication** - Secure registration and login with JWT tokens
- 📚 **Workshop Management** - Create, update, and delete workshops
- 👥 **Participant Management** - Join requests with approval workflow
- ✅ **Status Tracking** - Track workshop and participation status
- 🎯 **Owner Controls** - Approve/reject join requests, manage participants
- 📱 **Responsive UI** - Modern, mobile-friendly interface

## Tech Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **Database**: MySQL 8.0+
- **Authentication**: JWT with bcrypt
- **Testing**: pytest (135 tests)

### Frontend
- **Framework**: Next.js 13 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Testing**: Jest + React Testing Library

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 8.0+

### 1. Database Setup
```bash
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
JWT_SECRET_KEY=your-super-secret-key-change-in-production
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

Backend runs on http://localhost:3535

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

Frontend runs on http://localhost:3000

## Usage

### For Users

1. **Sign Up** - Create an account at `/auth/signup`
2. **Create Workshop** - Go to dashboard and click "Create Workshop"
3. **Browse Workshops** - View all workshops at `/workshops`
4. **Join Workshop** - Click "Join" on any workshop
5. **Manage Workshops** - View and manage your workshops in dashboard

### For Workshop Owners

1. **View Pending Requests** - See join requests in workshop detail page
2. **Approve/Reject** - Click approve or reject on pending requests
3. **Manage Participants** - Remove participants if needed
4. **Update Workshop** - Edit title, description, status, and signup settings

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

### Quick API Examples

**Register User**
```bash
curl -X POST http://localhost:3535/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
```

**Create Workshop**
```bash
curl -X POST http://localhost:3535/api/workshops \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Python Workshop",
    "description": "Learn Python basics"
  }'
```

## Project Structure

```
workshop-management/
├── backend/
│   ├── app/
│   │   ├── auth/           # Authentication services
│   │   ├── database/       # Database connection
│   │   ├── routes/         # API endpoints
│   │   ├── store/          # Data access layer
│   │   └── validators.py   # Input validation
│   ├── tests/              # Backend tests
│   └── requirements.txt
│
├── frontend/
│   ├── components/         # React components
│   ├── contexts/           # React contexts
│   ├── lib/                # Utility functions
│   ├── pages/              # Next.js pages
│   └── types/              # TypeScript types
│
└── docs/                   # Documentation
```

## Testing

### Backend Tests
```bash
cd backend
pytest                      # Run all tests
pytest -v                   # Verbose output
pytest --cov=app           # With coverage
```

**135 tests passing** covering:
- Authentication (57 tests)
- Workshops (26 tests)
- Participants (24 tests)
- Integration workflows (6 tests)

### Frontend Tests
```bash
cd frontend
npm test                    # Run all tests
npm run test:watch         # Watch mode
```

**6 test suites** covering:
- Auth components
- Dashboard components
- Workshop components

## Security

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with 30-minute expiration
- Protected API endpoints
- Input validation on frontend and backend
- SQL injection prevention
- CORS configuration

## Configuration

### Environment Variables

**Backend (.env)**
```
JWT_SECRET_KEY=your-secret-key
JWT_EXPIRATION_MINUTES=30
DB_HOST=localhost
DB_PORT=3306
DB_NAME=workshop_management
DB_USER=workshop_user
DB_PASSWORD=your-password
```

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=http://localhost:3535
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guide.

### Quick Deployment Checklist
- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure production database
- [ ] Enable HTTPS
- [ ] Update CORS origins
- [ ] Set up logging
- [ ] Configure backups
- [ ] Set up monitoring

## Documentation

### Quick Links
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[User Guide](USER_GUIDE.md)** - Complete user manual
- **[API Documentation](API_DOCUMENTATION.md)** - Full API reference

### For Developers
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Development setup and guidelines
- **[Testing Guide](TESTING_COMPLETE.md)** - Testing documentation
- **[Project Summary](PROJECT_COMPLETE.md)** - Complete project overview

### For Deployment
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions:
- Check the [documentation](docs/)
- Review [existing issues](https://github.com/yourusername/workshop-management/issues)
- Create a new issue if needed

## Acknowledgments

- Built with Flask, Next.js, and MySQL
- UI styled with Tailwind CSS
- Testing with pytest and Jest

---

**Status**: Production Ready ✅  
**Version**: 1.0.0  
**Last Updated**: March 2026
