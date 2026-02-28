# Learning Features Quick Start Guide

## Setup

### 1. Run Database Migration
```bash
cd backend
python migrate_db.py
```

### 2. Start Backend Server
```bash
cd backend
python run.py
```

Server runs on `http://localhost:3535`

### 3. Test the New Endpoints

## Workshop Owner Workflow

### Step 1: Create a Workshop with Date and Venue
```bash
curl -X POST http://localhost:3535/api/workshops \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Bootcamp 2026",
    "description": "Learn Python from scratch",
    "workshop_date": "2026-04-15",
    "venue_type": "physical",
    "venue_address": "123 Tech Street, San Francisco, CA"
  }'
```

Response:
```json
{
  "id": "workshop-uuid",
  "title": "Python Bootcamp 2026",
  "description": "Learn Python from scratch",
  "workshop_date": "2026-04-15",
  "venue_type": "physical",
  "venue_address": "123 Tech Street, San Francisco, CA",
  "status": "pending",
  "signup_enabled": true,
  "owner_id": "your-user-id",
  "created_at": "2026-03-01T10:00:00",
  "updated_at": "2026-03-01T10:00:00"
}
```

### Step 2: Add Lessons
```bash
curl -X POST http://localhost:3535/workshops/WORKSHOP_ID/lessons \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lesson 1: Python Basics",
    "description": "Introduction to Python syntax",
    "content": "Python is a high-level programming language...",
    "order_index": 1,
    "points": 10
  }'
```

### Step 3: Add Materials to Lesson
```bash
# Add video
curl -X POST http://localhost:3535/lessons/LESSON_ID/materials \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "material_type": "video",
    "title": "Python Basics Video Tutorial",
    "url": "https://youtube.com/watch?v=xyz",
    "duration": 1800
  }'

# Add PDF
curl -X POST http://localhost:3535/lessons/LESSON_ID/materials \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "material_type": "pdf",
    "title": "Python Cheat Sheet",
    "url": "https://example.com/python-cheatsheet.pdf",
    "file_size": 2048000
  }'
```

### Step 4: Create Challenges
```bash
curl -X POST http://localhost:3535/workshops/WORKSHOP_ID/challenges \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Challenge 1: FizzBuzz",
    "description": "Write a function that prints FizzBuzz",
    "html_content": "<p>Write a function that prints numbers 1-100...</p>",
    "solution": "def fizzbuzz():\n    for i in range(1, 101):\n        ...",
    "order_index": 1,
    "points": 20
  }'
```

### Step 5: Create Exam
```bash
# Create exam
curl -X POST http://localhost:3535/workshops/WORKSHOP_ID/exams \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Basics Quiz",
    "description": "Test your Python knowledge",
    "duration_minutes": 30,
    "passing_score": 70,
    "points": 50
  }'

# Add questions
curl -X POST http://localhost:3535/exams/EXAM_ID/questions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "What is the output of print(2 + 2)?",
    "question_type": "multiple_choice",
    "options": ["2", "4", "22", "Error"],
    "correct_answer": "4",
    "points": 10,
    "order_index": 1
  }'
```

### Step 6: Review Submissions
```bash
# Get challenge submissions
curl http://localhost:3535/challenges/CHALLENGE_ID/submissions \
  -H "Authorization: Bearer YOUR_TOKEN"

# Review a submission
curl -X POST http://localhost:3535/submissions/SUBMISSION_ID/review \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "passed",
    "points_earned": 20,
    "feedback": "Great work! Your solution is efficient."
  }'
```

## Participant Workflow

### Step 1: Join Workshop
```bash
curl -X POST http://localhost:3535/api/workshops/WORKSHOP_ID/join \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Step 2: View Lessons
```bash
curl http://localhost:3535/workshops/WORKSHOP_ID/lessons
```

Response includes lessons with materials:
```json
[
  {
    "id": "lesson-uuid",
    "title": "Lesson 1: Python Basics",
    "description": "Introduction to Python syntax",
    "content": "Python is...",
    "order_index": 1,
    "points": 10,
    "materials": [
      {
        "id": "material-uuid",
        "material_type": "video",
        "title": "Python Basics Video Tutorial",
        "url": "https://youtube.com/watch?v=xyz",
        "duration": 1800
      }
    ]
  }
]
```

### Step 3: Complete Lesson
```bash
curl -X POST http://localhost:3535/lessons/LESSON_ID/complete \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response:
```json
{
  "message": "Lesson completed",
  "points_earned": 10,
  "total_points": 10
}
```

### Step 4: Submit Challenge
```bash
curl -X POST http://localhost:3535/challenges/CHALLENGE_ID/submit \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "submission_text": "def fizzbuzz():\n    for i in range(1, 101):\n        if i % 15 == 0:\n            print(\"FizzBuzz\")\n        elif i % 3 == 0:\n            print(\"Fizz\")\n        elif i % 5 == 0:\n            print(\"Buzz\")\n        else:\n            print(i)",
    "submission_url": "https://github.com/user/fizzbuzz"
  }'
```

### Step 5: Take Exam
```bash
# Start exam
curl -X POST http://localhost:3535/exams/EXAM_ID/start \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response includes questions without answers
{
  "id": "attempt-uuid",
  "exam": {
    "id": "exam-uuid",
    "title": "Python Basics Quiz",
    "duration_minutes": 30,
    "questions": [
      {
        "id": "question-uuid",
        "question_text": "What is the output of print(2 + 2)?",
        "question_type": "multiple_choice",
        "options": ["2", "4", "22", "Error"],
        "points": 10
      }
    ]
  }
}

# Submit answers
curl -X POST http://localhost:3535/attempts/ATTEMPT_ID/submit \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "question-uuid": "4"
    }
  }'

# Response includes score and points
{
  "id": "attempt-uuid",
  "score": 100,
  "points_earned": 50,
  "passed": true,
  "submitted_at": "2026-03-01T11:00:00"
}
```

### Step 6: Check Progress
```bash
# Get my points
curl http://localhost:3535/me/points \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "points": {
    "user_id": "your-user-id",
    "total_points": 80,
    "lessons_completed": 1,
    "challenges_completed": 1,
    "exams_passed": 1,
    "current_rank": 5,
    "previous_rank": 8
  },
  "rank_info": {
    "rank": 5,
    "previous_rank": 8,
    "change": 3,
    "direction": "up",
    "total_points": 80
  }
}
```

## Leaderboard

### Global Leaderboard
```bash
curl http://localhost:3535/leaderboard?limit=10
```

Response:
```json
{
  "leaderboard": [
    {
      "user_id": "user-1",
      "name": "Alice",
      "total_points": 150,
      "lessons_completed": 5,
      "challenges_completed": 3,
      "exams_passed": 2,
      "current_rank": 1,
      "previous_rank": 2,
      "rank_info": {
        "rank": 1,
        "previous_rank": 2,
        "change": 1,
        "direction": "up"
      }
    },
    {
      "user_id": "user-2",
      "name": "Bob",
      "total_points": 120,
      "current_rank": 2,
      "previous_rank": 1,
      "rank_info": {
        "rank": 2,
        "previous_rank": 1,
        "change": 1,
        "direction": "down"
      }
    }
  ]
}
```

### Workshop Leaderboard
```bash
curl http://localhost:3535/workshops/WORKSHOP_ID/leaderboard
```

Response:
```json
{
  "workshop_id": "workshop-uuid",
  "workshop_title": "Python Bootcamp 2026",
  "leaderboard": [
    {
      "user_id": "user-1",
      "name": "Alice",
      "total_points": 80,
      "lessons_completed": 1,
      "challenges_completed": 1,
      "exams_passed": 1
    }
  ]
}
```

## Points Summary

| Activity | Default Points | Configurable |
|----------|---------------|--------------|
| Complete Lesson | 10 | ✅ Yes |
| Pass Challenge | 20 | ✅ Yes |
| Pass Exam | 50 | ✅ Yes |

## Rank Changes

- **🆕 New**: First time on leaderboard
- **⬆️ Up**: Rank improved (moved up)
- **⬇️ Down**: Rank decreased (moved down)
- **➡️ Same**: No change in rank

## Testing Checklist

- [ ] Create workshop with date and venue
- [ ] Add lesson with materials
- [ ] Create challenge with solution
- [ ] Create exam with questions
- [ ] Join workshop as participant
- [ ] Complete lesson and earn points
- [ ] Submit challenge
- [ ] Review challenge submission
- [ ] Take and pass exam
- [ ] Check points and rank
- [ ] View global leaderboard
- [ ] View workshop leaderboard
- [ ] Verify rank changes

## Troubleshooting

### Migration Issues
```bash
# If migration fails, check MySQL connection
mysql -u workshop_user -p workshop_management

# Verify tables exist
SHOW TABLES;

# Check specific table
DESCRIBE lessons;
```

### API Errors
- **401 Unauthorized**: Check JWT token
- **403 Forbidden**: Check user permissions (owner vs participant)
- **404 Not Found**: Verify IDs are correct
- **400 Bad Request**: Check request body format

### Points Not Updating
```bash
# Manually trigger ranking update
curl -X POST http://localhost:3535/leaderboard/update \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Next Steps

1. Test all endpoints manually
2. Write automated tests
3. Implement frontend UI
4. Add file upload
5. Add real-time updates
6. Add notifications

---

**Ready to use!** The backend is fully functional. Start testing with curl or Postman, then build the frontend UI.
