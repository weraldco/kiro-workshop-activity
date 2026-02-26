# Workshop Management API - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python app.py
```

Server runs at: `http://localhost:3535`

### 3. Test the API

```bash
# Create a workshop
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

# List all workshops
curl http://localhost:3535/api/workshop
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation including:
- All API endpoints with examples
- Validation rules
- Error handling
- Testing instructions
- Troubleshooting guide
- Architecture overview

## 🧪 Run Tests

```bash
pytest
```

Expected: 68 tests pass

## 🔧 Common Issues

**Port in use?** Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=5002, debug=True)
```

**Module not found?** Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/workshop` | Create workshop |
| GET | `/api/workshop` | List all workshops |
| GET | `/api/workshop/{id}` | Get specific workshop |
| POST | `/api/workshop/{id}/challenge` | Create challenge |
| POST | `/api/workshop/{id}/register` | Register participant |
| GET | `/api/workshop/registrations` | List registrations |

## ✅ Response Format

All responses use this format:

**Success:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message",
  "data": {}
}
```

## 💾 Data Storage

Data is stored in `workshop_data.json` (auto-created)

## 🎯 Next Steps

1. Read the full [README.md](README.md)
2. Check [verification_report.md](verification_report.md) for test results
3. Explore the code in `app/` directory
4. Run the test suite with `pytest`
