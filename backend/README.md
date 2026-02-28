# Workshop Management API - Python Backend

Flask-based REST API for managing workshops, participants, and challenges.

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
# Development mode
python run.py

# Production mode (with Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3535 'app:create_app()'
```

The API will be available at `http://localhost:3535`

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_workshop_routes.py
```

## API Endpoints

All endpoints are prefixed with `/api`

- `GET /api/workshops` - List all workshops
- `POST /api/workshops` - Create a workshop
- `PATCH /api/workshops/:id/status` - Update workshop status
- `PATCH /api/workshops/:id/signup-flag` - Toggle signup flag
- `POST /api/workshops/:id/signup` - Sign up for workshop
- `GET /api/workshops/:id/participants` - List participants
- `POST /api/workshops/:id/challenges` - Create challenge
- `GET /api/workshops/:id/challenges` - List challenges
- `GET /api/challenges/:id` - Get challenge details

## Data Storage

Workshop data is stored in `workshop_data.json` in this directory.

## Project Structure

```
backend/
├── app/
│   ├── routes/          # API route handlers
│   ├── store/           # Data persistence layer
│   ├── services/        # Business logic
│   ├── validators.py    # Input validation
│   └── __init__.py      # Flask app factory
├── tests/               # Test files
├── workshop_data.json   # Data storage
├── requirements.txt     # Python dependencies
└── run.py              # Application entry point
```
