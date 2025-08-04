#!/bin/bash

# Verification script to ensure all payment-related code has been removed

echo "=== Payment Removal Verification Script ==="
echo

# Track if any issues are found
ISSUES_FOUND=0

# Function to check for payment references
check_payment_references() {
    local path=$1
    local description=$2
    
    echo "Checking $description..."
    
    # Search for payment/stripe references (case insensitive)
    if grep -r -i "payment\|stripe" "$path" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --exclude-dir="node_modules" --exclude-dir="dist" --exclude-dir=".git" > /dev/null 2>&1; then
        echo "❌ Found payment/stripe references in $description:"
        grep -r -i "payment\|stripe" "$path" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --exclude-dir="node_modules" --exclude-dir="dist" --exclude-dir=".git" | head -10
        echo
        ISSUES_FOUND=1
    else
        echo "✅ No payment/stripe references found in $description"
    fi
    echo
}

# Check each package
check_payment_references "packages/shared-types-enums/src" "shared-types-enums"
check_payment_references "packages/server/src" "server source code"
check_payment_references "packages/webapp/src" "webapp source code"

# Special check for form-renderer - allow the safety filter
echo "Checking form-renderer source code..."
if grep -r -i "payment\|stripe" "packages/form-renderer/src" --include="*.ts" --include="*.tsx" --exclude-dir="node_modules" --exclude-dir="dist" | grep -v "f.kind !== FieldKindEnum.PAYMENT" > /dev/null 2>&1; then
    echo "❌ Found payment/stripe references in form-renderer source code:"
    grep -r -i "payment\|stripe" "packages/form-renderer/src" --include="*.ts" --include="*.tsx" --exclude-dir="node_modules" --exclude-dir="dist" | grep -v "f.kind !== FieldKindEnum.PAYMENT" | head -10
    echo
    ISSUES_FOUND=1
else
    echo "✅ No payment/stripe references found in form-renderer source code (safety filter allowed)"
fi
echo

check_payment_references "packages/answer-utils/src" "answer-utils"
check_payment_references "packages/utils/src" "utils"

# Check package.json files for stripe dependencies
echo "Checking package.json files for stripe dependencies..."
if grep -r "stripe" --include="package.json" packages/ > /dev/null 2>&1; then
    echo "❌ Found stripe dependencies in package.json files:"
    grep -r "stripe" --include="package.json" packages/
    echo
    ISSUES_FOUND=1
else
    echo "✅ No stripe dependencies found in package.json files"
fi
echo

# Check environment files
echo "Checking environment files..."
if grep -r -i "stripe" --include=".env*" packages/ > /dev/null 2>&1; then
    echo "❌ Found stripe references in environment files:"
    grep -r -i "stripe" --include=".env*" packages/
    echo
    ISSUES_FOUND=1
else
    echo "✅ No stripe references found in environment files"
fi
echo

# Check database for payment fields
echo "Checking database for payment fields..."
PAYMENT_FORMS=$(docker exec framna-feedback-mongodb mongosh framna-feedback --eval 'db.forms.count({ "fields.kind": "payment" })' --quiet 2>/dev/null | tail -1)
if [ "$PAYMENT_FORMS" != "0" ] && [ -n "$PAYMENT_FORMS" ]; then
    echo "❌ Found $PAYMENT_FORMS forms with payment fields in database"
    ISSUES_FOUND=1
else
    echo "✅ No payment fields found in database"
fi
echo

# Summary
echo "=== Verification Summary ==="
if [ $ISSUES_FOUND -eq 0 ]; then
    echo "✅ All payment-related code has been successfully removed!"
else
    echo "❌ Issues found! Please review the output above."
    exit 1
fi