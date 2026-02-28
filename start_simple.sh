#!/bin/bash

echo "=========================================="
echo "Workshop Management System - Simple Start"
echo "=========================================="
echo ""

# Start Backend
echo "Starting Backend..."
source venv/bin/activate
cd backend
python run.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../backend.pid
echo "✓ Backend started (PID: $BACKEND_PID)"
echo "  Log: tail -f backend.log"
cd ..
deactivate

# Wait for backend
sleep 3

# Start Frontend
echo ""
echo "Starting Frontend..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid
echo "✓ Frontend started (PID: $FRONTEND_PID)"
echo "  Log: tail -f frontend.log"
cd ..

echo ""
echo "=========================================="
echo "✓ Servers Started"
echo "=========================================="
echo ""
echo "Backend:  http://localhost:3535"
echo "Frontend: http://localhost:3000"
echo ""
echo "To stop: ./stop.sh"
echo ""
