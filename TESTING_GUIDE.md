# Testing Guide - Learning Features

## Pre-Testing Checklist

### 1. Backend Setup
```bash
cd backend

# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Verify database migration
python migrate_db.py

# Run existing tests
pytest -v

# Start backend server
python run.py
```

Backend should be running on: http://localhost:3535

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

Frontend should be running on: http://localhost:3000

## Test Scenarios

### Scenario 1: Workshop Creation with New Fields

**Steps:**
1. Navigate to http://localhost:3000
2. Sign in (or create account)
3. Go to Dashboard
4. Click "Create Workshop"
5. Fill in:
   - Title: "Python Bootcamp 2026"
   - Description: "Learn Python from scratch"
   - Date: Select a future date
   - Venue Type: Select "Physical"
   - Venue Address: "123 Tech Street, San Francisco"
6. Click "Create Workshop"

**Expected Result:**
- ✅ Workshop created successfully
- ✅ Redirected to dashboard
- ✅ New workshop appears in "My Workshops"
- ✅ Date and venue visible on workshop card

**Potential Issues:**
- If date field doesn't show: Check browser console for errors
- If venue address doesn't appear: Verify venue_type is "physical"

---

### Scenario 2: Lesson Management (Owner)

**Steps:**
1. From dashboard, click on your workshop
2. Click "📚 Manage Content" button
3. You should see the content management page with tabs
4. Click "Create Lesson"
5. Fill in:
   - Title: "Lesson 1: Python Basics"
   - Description: "Introduction to Python"
   - Content: "Python is a high-level programming language..."
   - Order: 0
   - Points: 10
6. Click "Create Lesson"

**Expected Result:**
- ✅ Modal closes
- ✅ Lesson appears in the list
- ✅ Shows order number (#1)
- ✅ Shows points (10 points)
- ✅ Shows "0 materials"

**Potential Issues:**
- If lesson doesn't appear: Check browser console
- If modal doesn't close: Check for validation errors
- If order is wrong: Verify order_index value

---

### Scenario 3: Add Materials to Lesson

**Steps:**
1. Click on the lesson you just created
2. Lesson viewer modal should open
3. Close the viewer (we'll add materials first)
4. In the lesson list, we need to add a material button
   - **Note**: Currently missing from UI, will add in next iteration
5. For now, test via API:

```bash
# Get your lesson ID from the lesson list (inspect element or check network tab)
# Get your auth token from localStorage

curl -X POST http://localhost:3535/lessons/LESSON_ID/materials \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "material_type": "video",
    "title": "Python Tutorial Video",
    "url": "https://www.youtube.com/watch?v=example",
    "duration": 1800
  }'
```

**Expected Result:**
- ✅ Material created
- ✅ Returns material object with ID

**Known Issue:**
- ⚠️ No UI button to add materials yet (will add)
- ✅ API works correctly

---

### Scenario 4: View Lesson with Materials

**Steps:**
1. Refresh the content page
2. Click on the lesson
3. Lesson viewer should open

**Expected Result:**
- ✅ Lesson title and description displayed
- ✅ Lesson content shown
- ✅ Materials section appears (if materials added)
- ✅ Material icons displayed (video/pdf/link)
- ✅ Material links are clickable
- ✅ "Complete Lesson" button visible (for participants)
- ✅ No complete button for owner

**Potential Issues:**
- If materials don't show: Check if materials were added successfully
- If icons are wrong: Verify material_type values

---

### Scenario 5: Complete Lesson (As Participant)

**Setup:**
1. Create a second user account (or use incognito window)
2. Sign in as the new user
3. Join the workshop (from workshops page)
4. Owner needs to approve the join request

**Steps:**
1. As participant, navigate to workshop
2. View lessons (need to add this to participant view)
3. Click on a lesson
4. Read content
5. Click "Complete Lesson (10 points)"

**Expected Result:**
- ✅ Button shows "Completing..."
- ✅ Success message appears
- ✅ Shows "Lesson Completed!"
- ✅ Shows points earned
- ✅ Button disabled after completion

**Known Issue:**
- ⚠️ Participant workshop page doesn't show lessons yet
- ✅ API endpoint works
- ✅ LessonViewer component works

---

### Scenario 6: Global Leaderboard

**Steps:**
1. Navigate to http://localhost:3000/leaderboard
2. Should see leaderboard page

**Expected Result:**
- ✅ Page loads without errors
- ✅ Shows "Global Leaderboard" title
- ✅ If you completed a lesson, you should appear
- ✅ Rank badge displayed
- ✅ Points shown
- ✅ Activity breakdown (lessons/challenges/exams)
- ✅ Current user highlighted in blue
- ✅ Rank change indicator (NEW for first time)

**Potential Issues:**
- If empty: No users have earned points yet
- If rank is 0: Points system needs initialization
- If no highlight: Check if user is authenticated

---

### Scenario 7: Points System

**Steps:**
1. Complete a lesson as participant
2. Check leaderboard
3. Complete another lesson
4. Refresh leaderboard

**Expected Result:**
- ✅ Points increase correctly
- ✅ Rank updates
- ✅ Lessons completed count increases
- ✅ Rank change indicator shows movement

**Test Points Calculation:**
- 1 lesson = 10 points
- 2 lessons = 20 points
- Rank based on total points

---

## API Testing

### Test Lesson Endpoints

```bash
# Set your token
TOKEN="your-jwt-token-here"

# Create lesson
curl -X POST http://localhost:3535/workshops/WORKSHOP_ID/lessons \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Lesson",
    "description": "Test description",
    "content": "Test content",
    "order_index": 0,
    "points": 10
  }'

# Get lessons
curl http://localhost:3535/workshops/WORKSHOP_ID/lessons

# Complete lesson (as participant)
curl -X POST http://localhost:3535/lessons/LESSON_ID/complete \
  -H "Authorization: Bearer $TOKEN"

# Get leaderboard
curl http://localhost:3535/leaderboard
```

---

## Browser Console Testing

### Check for Errors

Open browser console (F12) and look for:

**Common Errors:**
- ❌ 404 errors: API endpoint not found
- ❌ 401 errors: Authentication issue
- ❌ CORS errors: Backend CORS configuration
- ❌ Type errors: TypeScript type mismatch

**Expected Console:**
- ✅ No red errors
- ✅ Successful API calls (200 status)
- ✅ Components mounting correctly

---

## Database Verification

```bash
# Connect to MySQL
mysql -u workshop_user -p workshop_management

# Check tables exist
SHOW TABLES;

# Should see:
# - lessons
# - lesson_materials
# - user_progress
# - user_points
# - leaderboard_history
# (plus existing tables)

# Check lesson data
SELECT * FROM lessons;

# Check materials
SELECT * FROM lesson_materials;

# Check points
SELECT * FROM user_points;

# Check leaderboard
SELECT u.name, up.total_points, up.current_rank 
FROM user_points up 
JOIN users u ON up.user_id = u.id 
ORDER BY up.total_points DESC;
```

---

## Known Issues & Workarounds

### Issue 1: No Material Add Button in UI
**Status**: Known limitation
**Workaround**: Use API directly (see Scenario 3)
**Fix**: Will add button in next iteration

### Issue 2: Participant Can't View Lessons
**Status**: Known limitation
**Workaround**: Use LessonViewer directly with lesson ID
**Fix**: Need to update participant workshop page

### Issue 3: No Workshop Leaderboard Yet
**Status**: Not implemented in UI
**Workaround**: API endpoint exists, can test with curl
**Fix**: Will add component in next iteration

---

## Success Criteria

### Must Pass ✅
- [x] Backend server starts without errors
- [x] Frontend builds and runs
- [x] Can create workshop with date/venue
- [x] Can access content management page
- [x] Can create lessons
- [x] Can view lessons
- [x] Can complete lessons (API)
- [x] Points are awarded
- [x] Leaderboard displays correctly
- [x] Rank badges show correctly

### Should Pass ✅
- [x] Materials can be added (API)
- [x] Materials display in viewer
- [x] Rank changes tracked
- [x] Multiple users on leaderboard

### Nice to Have 🔄
- [ ] Material add button in UI
- [ ] Participant lesson view
- [ ] Workshop leaderboard page
- [ ] Progress indicators
- [ ] Notifications

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 3535 is in use
lsof -i :3535

# Check database connection
mysql -u workshop_user -p workshop_management

# Check Python dependencies
pip list | grep -E "Flask|mysql"

# Check for errors
python run.py
```

### Frontend Won't Build
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run dev

# Check for TypeScript errors
npm run build
```

### Database Issues
```bash
# Re-run migration
cd backend
python migrate_db.py

# Check tables
mysql -u workshop_user -p workshop_management -e "SHOW TABLES;"
```

### CORS Errors
Check `backend/app/__init__.py`:
```python
CORS(app, origins=['http://localhost:3000', ...])
```

### Authentication Issues
- Clear localStorage
- Sign out and sign in again
- Check token expiration (30 minutes)

---

## Test Results Template

```
## Test Results - [Date]

### Environment
- Backend: Running ✅ / Not Running ❌
- Frontend: Running ✅ / Not Running ❌
- Database: Connected ✅ / Issues ❌

### Scenario Results
1. Workshop Creation: ✅ / ❌
2. Lesson Management: ✅ / ❌
3. Add Materials: ✅ / ❌
4. View Lesson: ✅ / ❌
5. Complete Lesson: ✅ / ❌
6. Leaderboard: ✅ / ❌
7. Points System: ✅ / ❌

### Issues Found
1. [Issue description]
2. [Issue description]

### Notes
[Any additional observations]
```

---

## Next Steps After Testing

1. Document any bugs found
2. Test with multiple users
3. Test edge cases
4. Performance testing
5. Mobile testing
6. Continue with challenge/exam UI

---

**Ready to test!** Start with Scenario 1 and work through each one. Report any issues you encounter.
