#!/bin/bash

# Workshop Management System - Stop Script
# This script stops both backend and frontend servers

echo "=========================================="
echo "Stopping Workshop Management System"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Stop Backend
if [ -f backend.pid ]; then
    BACKEND_PID=$(cat backend.pid)
    echo "Stopping backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Backend stopped${NC}"
    else
        echo -e "${RED}Backend process not found${NC}"
    fi
    rm backend.pid
else
    echo "No backend PID file found"
fi

# Stop Frontend
if [ -f frontend.pid ]; then
    FRONTEND_PID=$(cat frontend.pid)
    echo "Stopping frontend (PID: $FRONTEND_PID)..."
    kill $FRONTEND_PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    else
        echo -e "${RED}Frontend process not found${NC}"
    fi
    rm frontend.pid
else
    echo "No frontend PID file found"
fi

# Kill any remaining processes on the ports
echo ""
echo "Checking for remaining processes..."

# Check port 3535 (backend)
BACKEND_PROC=$(lsof -ti:3535)
if [ ! -z "$BACKEND_PROC" ]; then
    echo "Killing process on port 3535..."
    kill -9 $BACKEND_PROC 2>/dev/null
    echo -e "${GREEN}✓ Port 3535 cleared${NC}"
fi

# Check port 3000 (frontend)
FRONTEND_PROC=$(lsof -ti:3000)
if [ ! -z "$FRONTEND_PROC" ]; then
    echo "Killing process on port 3000..."
    kill -9 $FRONTEND_PROC 2>/dev/null
    echo -e "${GREEN}✓ Port 3000 cleared${NC}"
fi

echo ""
echo -e "${GREEN}All servers stopped${NC}"
