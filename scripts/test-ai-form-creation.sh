#!/bin/bash

# Test script for AI form creation with proper authentication
# This script helps debug the create-form-with-ai resolver

# Configuration
API_URL="http://localhost:9157/graphql"
EMAIL="${TEST_EMAIL:-test@example.com}"
PASSWORD="${TEST_PASSWORD:-password123}"
PROJECT_ID="${PROJECT_ID}"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AI Form Creation Test Script${NC}"
echo "================================"

# Function to login and get session cookie
login() {
    echo -e "\n${BLUE}Step 1: Logging in...${NC}"
    
    RESPONSE=$(curl -s -c cookies.txt -w "\n%{http_code}" \
        -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "X-Device-Id: test-device-$(date +%s)" \
        -d '{
            "query": "query login($input: LoginInput!) { login(input: $input) }",
            "variables": {
                "input": {
                    "email": "'$EMAIL'",
                    "password": "'$PASSWORD'"
                }
            }
        }')
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✓ Login successful${NC}"
        echo "Response: $BODY"
        
        # Extract session cookie
        SESSION_COOKIE=$(grep "HEYFORM_SESSION" cookies.txt | awk '{print $7}')
        if [ -n "$SESSION_COOKIE" ]; then
            echo -e "${GREEN}✓ Session cookie obtained${NC}"
            return 0
        else
            echo -e "${RED}✗ Failed to get session cookie${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Login failed (HTTP $HTTP_CODE)${NC}"
        echo "Response: $BODY"
        return 1
    fi
}

# Function to create form with AI
create_form_with_ai() {
    echo -e "\n${BLUE}Step 2: Creating form with AI...${NC}"
    
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}✗ PROJECT_ID not set. Run: ./scripts/get-project-id.sh${NC}"
        return 1
    fi
    
    echo "Using Project ID: $PROJECT_ID"
    echo "Topic: Customer satisfaction survey for a coffee shop"
    
    # Extract device ID from cookies
    DEVICE_ID=$(grep "HEYFORM_DEVICE_ID" cookies.txt | awk '{print $7}' || echo "test-device-$(date +%s)")
    
    RESPONSE=$(curl -s -b cookies.txt -w "\n%{http_code}" \
        -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "X-Device-Id: $DEVICE_ID" \
        -d '{
            "query": "mutation createFormWithAI($input: CreateFormWithAIInput!) { createFormWithAI(input: $input) }",
            "variables": {
                "input": {
                    "projectId": "'$PROJECT_ID'",
                    "topic": "Customer satisfaction survey for a coffee shop",
                    "reference": "Include questions about service quality, product variety, and ambiance"
                }
            }
        }')
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✓ Form creation request sent${NC}"
        echo "Response: $BODY"
        
        # Extract form ID from response
        FORM_ID=$(echo "$BODY" | grep -o '"createFormWithAI":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$FORM_ID" ]; then
            echo -e "${GREEN}✓ Form created with ID: $FORM_ID${NC}"
            return 0
        fi
    else
        echo -e "${RED}✗ Form creation failed (HTTP $HTTP_CODE)${NC}"
        echo "Response: $BODY"
        return 1
    fi
}

# Function to test with custom data
test_custom() {
    local topic="$1"
    local reference="$2"
    
    echo -e "\n${BLUE}Testing with custom topic...${NC}"
    echo "Topic: $topic"
    echo "Reference: $reference"
    
    RESPONSE=$(curl -s -b cookies.txt -w "\n%{http_code}" \
        -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "X-Device-Id: $(grep "HEYFORM_DEVICE_ID" cookies.txt | awk '{print $7}' || echo "test-device-$(date +%s)")" \
        -d '{
            "query": "mutation createFormWithAI($input: CreateFormWithAIInput!) { createFormWithAI(input: $input) }",
            "variables": {
                "input": {
                    "projectId": "'$PROJECT_ID'",
                    "topic": "'"$topic"'",
                    "reference": "'"$reference"'"
                }
            }
        }')
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    echo "Response: $BODY"
}

# Main execution
main() {
    # Check if server is running
    if ! curl -s -o /dev/null "http://localhost:9157"; then
        echo -e "${RED}✗ Server is not running on port 9157${NC}"
        echo "Start the server with: pnpm dev:server"
        exit 1
    fi
    
    # Login
    if login; then
        # Create form with AI
        create_form_with_ai
        
        # Offer custom test
        echo -e "\n${BLUE}Do you want to test with custom data? (y/n)${NC}"
        read -r answer
        if [ "$answer" = "y" ]; then
            echo "Enter topic:"
            read -r custom_topic
            echo "Enter reference (optional):"
            read -r custom_reference
            test_custom "$custom_topic" "$custom_reference"
        fi
    fi
    
    # Cleanup
    rm -f cookies.txt
}

# Show usage
if [ "$1" = "--help" ]; then
    echo "Usage: $0"
    echo ""
    echo "Environment variables:"
    echo "  TEST_EMAIL     - Email for login (default: test@example.com)"
    echo "  TEST_PASSWORD  - Password for login (default: password123)"
    echo "  PROJECT_ID     - Project ID to use for form creation"
    echo ""
    echo "Example:"
    echo "  PROJECT_ID=507f1f77bcf86cd799439011 $0"
    exit 0
fi

# Run main function
main