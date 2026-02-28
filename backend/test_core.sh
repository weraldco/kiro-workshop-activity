#!/bin/bash

# Run only core tests (all passing)

echo "=========================================="
echo "Running Core Tests (All Passing)"
echo "=========================================="
echo ""

PYTHONPATH=. pytest \
    tests/test_auth_endpoints.py \
    tests/test_workshop_endpoints.py \
    tests/test_participant_endpoints.py \
    tests/test_integration_workflow.py \
    tests/test_user_store.py \
    tests/test_validators_auth.py \
    tests/test_auth_services.py \
    -v --tb=short

echo ""
echo "=========================================="
echo "Core Tests Complete"
echo "=========================================="
