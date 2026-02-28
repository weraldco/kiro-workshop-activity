#!/bin/bash

# Workshop Management System - Start Script
# This script starts both backend and frontend servers

echo "=========================================="
echo "Workshop Management System"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo -e "${RED}Error: backend directory not found${NC}"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${RED}Error: frontend directory not found${NC}"
    exit 1
fi

# Function to check if port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Check if ports are available
echo -e "${BLUE}Checking ports...${NC}"
if check_port 3535; then
    echo -e "${RED}Port 3535 is already in use (backend)${NC}"
    echo "Please stop the process using port 3535 or run: lsof -ti:3535 | xargs kill"
    exit 1
fi

if check_port 3000; then
    echo -e "${RED}Port 3000 is already in use (frontend)${NC}"
    echo "Please stop the process using port 3000 or run: lsof -ti:3000 | xargs kill"
    exit 1
fi

echo -e "${GREEN}✓ Ports available${NC}"
echo ""

# Start Backend
echo -e "${BLUE}Starting Backend Server...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${BLUE}Installing backend dependencies...${NC}"
    pip install -r requirements.txt
fi

# Check database connection
echo -e "${BLUE}Checking database connection...${NC}"
python -c "import sys; sys.path.insert(0, 'backend'); from app.database.connection import test_connection; test_connection()" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Database connection failed. Please check your MySQL setup.${NC}"
    echo "Run: mysql -u root -p"
    echo "Then: CREATE DATABASE workshop_management;"
    exit 1
fi

echo -e "${GREEN}✓ Database connected${NC}"

# Start backend in background
echo -e "${BLUE}Starting Flask server on port 3535...${NC}"
python run.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../backend.pid
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

cd ..

# Wait a moment for backend to start
sleep 2

# Start Frontend
echo -e "${BLUE}Starting Frontend Server...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    npm install
fi

# Start frontend in background
echo -e "${BLUE}Starting Next.js server on port 3000...${NC}"
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

cd ..

# Wait for servers to be ready
echo ""
echo -e "${BLUE}Waiting for servers to be ready...${NC}"
sleep 5

# Check if servers are running
if check_port 3535 && check_port 3000; then
    echo ""
    echo -e "${GREEN}=========================================="
    echo "✓ All servers started successfully!"
    echo "==========================================${NC}"
    echo ""
    echo -e "${BLUE}Backend:${NC}  http://localhost:3535"
    echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
    echo ""
    echo -e "${BLUE}Logs:${NC}"
    echo "  Backend:  tail -f backend.log"
    echo "  Frontend: tail -f frontend.log"
    echo ""
    echo -e "${BLUE}To stop servers:${NC}"
    echo "  ./stop.sh"
    echo ""
    echo -e "${GREEN}Ready to use!${NC}"
else
    echo -e "${RED}Error: Servers failed to start${NC}"
    echo "Check logs:"
    echo "  Backend:  cat backend.log"
    echo "  Frontend: cat frontend.log"
    
    # Cleanup
    if [ -f backend.pid ]; then
        kill $(cat backend.pid) 2>/dev/null
        rm backend.pid
    fi
    if [ -f frontend.pid ]; then
        kill $(cat frontend.pid) 2>/dev/null
        rm frontend.pid
    fi
    exit 1
fi
