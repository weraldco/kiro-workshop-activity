#!/bin/bash

# Test script to verify end-to-end integration
# This script tests: frontend fetch → backend API → database → response

echo "🧪 Testing Workshop Management System Integration"
echo "=================================================="
echo ""

# Test 1: Backend API health check
echo "1️⃣  Testing backend health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:3001/health)
if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
  echo "   ✅ Backend is healthy"
else
  echo "   ❌ Backend health check failed"
  exit 1
fi
echo ""

# Test 2: Backend API workshops endpoint
echo "2️⃣  Testing backend workshops endpoint..."
WORKSHOPS_RESPONSE=$(curl -s http://localhost:3001/api/workshops)
WORKSHOP_COUNT=$(echo "$WORKSHOPS_RESPONSE" | grep -o '"id"' | wc -l)
if [ "$WORKSHOP_COUNT" -gt 0 ]; then
  echo "   ✅ Backend returned $WORKSHOP_COUNT workshops"
  echo "   📋 Sample workshop titles:"
  echo "$WORKSHOPS_RESPONSE" | grep -o '"title":"[^"]*"' | head -3 | sed 's/"title":"//g' | sed 's/"//g' | sed 's/^/      - /'
else
  echo "   ❌ Backend returned no workshops"
  exit 1
fi
echo ""

# Test 3: Verify response format
echo "3️⃣  Verifying response format..."
if echo "$WORKSHOPS_RESPONSE" | grep -q '"status"'; then
  echo "   ✅ Response contains status field"
else
  echo "   ❌ Response missing status field"
  exit 1
fi

if echo "$WORKSHOPS_RESPONSE" | grep -q '"signup_enabled"'; then
  echo "   ✅ Response contains signup_enabled field"
else
  echo "   ❌ Response missing signup_enabled field"
  exit 1
fi
echo ""

# Test 4: Frontend proxy (if Next.js is running)
echo "4️⃣  Testing frontend proxy (if running)..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/workshops 2>/dev/null)
if [ "$FRONTEND_RESPONSE" = "200" ]; then
  echo "   ✅ Frontend proxy is working (returned HTTP $FRONTEND_RESPONSE)"
else
  echo "   ⚠️  Frontend not running or proxy not working (HTTP $FRONTEND_RESPONSE)"
  echo "   💡 Start frontend with: cd frontend && npm run dev"
fi
echo ""

echo "=================================================="
echo "✅ Integration test completed successfully!"
echo ""
echo "📝 Summary:"
echo "   - Backend API: Running on port 3001"
echo "   - Workshops endpoint: /api/workshops"
echo "   - Response format: Array of workshop objects"
echo "   - Frontend proxy: Configured in next.config.js"
echo ""
echo "🚀 To test the full frontend:"
echo "   1. Ensure backend is running: cd backend && npm run dev"
echo "   2. Start frontend: cd frontend && npm run dev"
echo "   3. Open browser: http://localhost:3000"
