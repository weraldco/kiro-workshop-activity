#!/bin/bash

# Workshop Management System - Test Script
# This script runs all tests

echo "=========================================="
echo "Workshop Management System - Test Suite"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Backend Tests
echo -e "${BLUE}Running Backend Tests...${NC}"
echo ""

cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}Virtual environment not found${NC}"
    exit 1
fi

# Run pytest
echo "Running pytest..."
python -m pytest tests/ -v --tb=short

BACKEND_RESULT=$?

cd ..

echo ""
echo "=========================================="
echo -e "${BLUE}Test Summary${NC}"
echo "=========================================="
echo ""

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All backend tests passed${NC}"
else
    echo -e "${RED}✗ Some backend tests failed${NC}"
    echo "Check output above for details"
fi

echo ""
echo "Frontend tests: Run 'cd frontend && npm test'"
echo ""

exit $BACKEND_RESULT
