# Quick Reference Guide

## Starting the System

```bash
# Start both backend and frontend
./start.sh

# Or manually:
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Stopping the System

```bash
./stop.sh
```

## Running Tests

```bash
# All backend tests
./test.sh

# Or manually
cd backend
source venv/bin/activate
pytest -v

# Frontend tests
cd frontend
npm test
```

## URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3535
- **Leaderboard**: http://localhost:3000/leaderboard

## Quick Actions

### Create Workshop with Date/Venue
1. Sign in
2. Go to Dashboard
3. Click "Create Workshop"
4. Fill in title, description, date, venue type, address
5. Submit

### Manage Lesson Content
1. Go to your workshop
2. Click "📚 Manage Content"
3. Click "Create Lesson"
4. Fill in lesson details
5. Submit

### View Leaderboard
1. Navigate to http://localhost:3000/leaderboard
2. See your rank and points
3. Check rank changes (↑ up, ↓ down)

## API Quick Reference

### Authentication
```bash
# Register
curl -X POST http://localhost:3535/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123!","name":"User"}'

# Login
curl -X POST http://localhost:3535/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123!"}'
```

### Lessons
```bash
# Create lesson
curl -X POST http://localhost:3535/workshops/{id}/lessons \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Lesson 1","description":"Intro","content":"Content","points":10}'

# List lessons
curl http://localhost:3535/workshops/{id}/lessons

# Complete lesson
curl -X POST http://localhost:3535/lessons/{id}/complete \
  -H "Authorization: Bearer {token}"
```

### Leaderboard
```bash
# Global leaderboard
curl http://localhost:3535/leaderboard

# My points
curl http://localhost:3535/me/points \
  -H "Authorization: Bearer {token}"
```

## Database Commands

```bash
# Connect to database
mysql -u workshop_user -p workshop_management

# Check tables
SHOW TABLES;

# View lessons
SELECT * FROM lessons;

# View points
SELECT u.name, up.total_points, up.current_rank 
FROM user_points up 
JOIN users u ON up.user_id = u.id 
ORDER BY up.total_points DESC;

# View leaderboard history
SELECT * FROM leaderboard_history ORDER BY recorded_at DESC LIMIT 10;
```

## Troubleshooting

### Backend won't start
```bash
# Check port
lsof -i :3535

# Check database
mysql -u workshop_user -p workshop_management

# Check logs
cat backend.log
```

### Frontend won't start
```bash
# Check port
lsof -i :3000

# Clear cache
cd frontend
rm -rf .next node_modules
npm install

# Check logs
cat frontend.log
```

### Database issues
```bash
# Re-run migration
cd backend
python migrate_db.py

# Check connection
python -c "from app.database.connection import test_connection; test_connection()"
```

## File Locations

### Backend
- **Main app**: `backend/app/__init__.py`
- **Routes**: `backend/app/routes/`
- **Stores**: `backend/app/store/`
- **Tests**: `backend/tests/`
- **Config**: `backend/.env`

### Frontend
- **Pages**: `frontend/pages/`
- **Components**: `frontend/components/`
- **API**: `frontend/lib/`
- **Types**: `frontend/types/`
- **Config**: `frontend/.env.local`

## Common Tasks

### Add a new lesson
1. Go to workshop content page
2. Click "Create Lesson"
3. Fill form
4. Submit

### Add material to lesson
```bash
# Via API (UI button coming soon)
curl -X POST http://localhost:3535/lessons/{id}/materials \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"material_type":"video","title":"Tutorial","url":"https://..."}'
```

### Check user points
```bash
curl http://localhost:3535/me/points \
  -H "Authorization: Bearer {token}"
```

### Update rankings
```bash
curl -X POST http://localhost:3535/leaderboard/update \
  -H "Authorization: Bearer {token}"
```

## Points System

- **Lesson completion**: 10 points (default)
- **Challenge passed**: 20 points (default)
- **Exam passed**: 50 points (default)

Points are configurable when creating content.

## Rank Indicators

- 🆕 **NEW**: First time on leaderboard
- ⬆️ **UP**: Rank improved
- ⬇️ **DOWN**: Rank decreased
- ➡️ **SAME**: No change

## Status Codes

- **200**: Success
- **201**: Created
- **400**: Bad request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not found
- **500**: Server error

## Environment Variables

### Backend (.env)
```
JWT_SECRET_KEY=your-secret-key
JWT_EXPIRATION_MINUTES=30
DB_HOST=localhost
DB_PORT=3306
DB_NAME=workshop_management
DB_USER=workshop_user
DB_PASSWORD=password1
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:3535
```

## Useful Commands

```bash
# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# Check running processes
ps aux | grep python
ps aux | grep node

# Kill process on port
lsof -ti:3535 | xargs kill
lsof -ti:3000 | xargs kill

# Database backup
mysqldump -u workshop_user -p workshop_management > backup.sql

# Database restore
mysql -u workshop_user -p workshop_management < backup.sql
```

## Documentation

- **README.md**: Main project documentation
- **TESTING_GUIDE.md**: Comprehensive testing guide
- **TEST_RESULTS.md**: Latest test results
- **IMPLEMENTATION_COMPLETE.md**: Feature completion status
- **LEARNING_FEATURES_QUICKSTART.md**: Quick start for new features
- **API_DOCUMENTATION.md**: Full API reference

## Support

For issues:
1. Check logs (backend.log, frontend.log)
2. Check browser console (F12)
3. Check database connection
4. Review documentation
5. Check TEST_RESULTS.md for known issues

---

**Quick Start**: `./start.sh` → Visit http://localhost:3000
**Quick Stop**: `./stop.sh`
**Quick Test**: `./test.sh`
