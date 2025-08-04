#!/bin/bash

echo "🔍 Testing login functionality..."
echo ""

# Test credentials
EMAIL="test@example.com"
PASSWORD="Test123!"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test GraphQL endpoint
echo "1. Testing GraphQL endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:9157/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __typename }"}'
)

if [[ $RESPONSE == *"__typename"* ]]; then
  echo -e "${GREEN}✓ GraphQL endpoint is responding${NC}"
else
  echo -e "${RED}✗ GraphQL endpoint is not responding${NC}"
  echo "Response: $RESPONSE"
  exit 1
fi

echo ""
echo "2. Testing login mutation..."

# Login mutation - properly escaped
LOGIN_QUERY='mutation { login(input: { email: \"'$EMAIL'\", password: \"'$PASSWORD'\" }) }'

echo "Sending login request..."
RESPONSE=$(curl -s -X POST http://localhost:9157/graphql \
  -H "Content-Type: application/json" \
  -H "x-device-id: test-device-$(date +%s)" \
  -d "{\"query\":\"$LOGIN_QUERY\"}" \
  -c /tmp/cookies.txt \
  -w "\n\nHTTP_CODE:%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

echo ""
echo "Response status: $HTTP_CODE"
echo "Response body: $BODY"

if [[ $HTTP_CODE == "200" ]] && [[ $BODY == *"true"* ]]; then
  echo -e "${GREEN}✓ Login successful${NC}"
  echo ""
  echo "3. Checking cookies..."
  if [ -f /tmp/cookies.txt ]; then
    echo "Cookies saved:"
    cat /tmp/cookies.txt | grep -E "session|auth"
  fi
else
  echo -e "${RED}✗ Login failed${NC}"
  
  # Check for common issues
  echo ""
  echo -e "${YELLOW}Debugging tips:${NC}"
  echo "1. Check if MongoDB is running: docker ps | grep mongo"
  echo "2. Check if Redis is running: docker ps | grep redis"
  echo "3. Check server logs: Look for errors in the terminal running 'pnpm dev:server'"
  echo "4. Verify test user exists: ./mongodb-utils.sh users"
fi

# Cleanup
rm -f /tmp/cookies.txt

echo ""
echo "4. Testing from frontend proxy..."
curl -s -X POST http://localhost:3000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __typename }"}' \
  -o /dev/null -w "Frontend proxy status: %{http_code}\n"