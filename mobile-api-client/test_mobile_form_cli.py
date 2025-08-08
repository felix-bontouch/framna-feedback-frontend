#!/usr/bin/env python3
"""Test script for Mobile API Client"""

import json
import time
from mobile_api_client import MobileAPIClient
from exceptions import ValidationError, MobileAPIError


def create_test_form_data():
    """Create a test form structure for testing"""
    return {
        "id": "test-form-123",
        "teamId": "team123",
        "projectId": "proj456",
        "name": "Test Customer Feedback Survey",
        "description": "Help us test our mobile API",
        "interactiveMode": 1,
        "kind": 1,
        "settings": {
            "active": True,
            "captchaKind": "none",
            "requirePassword": False,
            "redirectOnCompletion": True,
            "redirectUrl": "https://example.com/thank-you",
            "filterSpam": False,
            "allowArchive": True,
            "locale": "en",
            "languages": ["en"],
            "enableQuotaLimit": False,
            "quotaLimit": 0,
            "enableIpLimit": False,
            "ipLimitCount": 3
        },
        "fields": [
            {
                "id": "field1",
                "kind": "short_text",
                "title": "What's your name?",
                "description": "Please enter your full name",
                "validations": {
                    "required": True,
                    "minLength": 2,
                    "maxLength": 100
                },
                "properties": {
                    "placeholder": "John Doe"
                }
            },
            {
                "id": "field2",
                "kind": "email",
                "title": "Your email address",
                "validations": {
                    "required": True
                },
                "properties": {
                    "placeholder": "john@example.com"
                }
            },
            {
                "id": "field3",
                "kind": "multiple_choice",
                "title": "How satisfied are you?",
                "validations": {
                    "required": True
                },
                "properties": {
                    "choices": [
                        {"id": "choice1", "label": "Very Satisfied", "score": 5},
                        {"id": "choice2", "label": "Satisfied", "score": 4},
                        {"id": "choice3", "label": "Neutral", "score": 3},
                        {"id": "choice4", "label": "Dissatisfied", "score": 2},
                        {"id": "choice5", "label": "Very Dissatisfied", "score": 1}
                    ],
                    "allowMultiple": False,
                    "allowOther": True
                }
            },
            {
                "id": "field4",
                "kind": "rating",
                "title": "Rate our service",
                "validations": {
                    "required": True
                },
                "properties": {
                    "total": 10
                }
            },
            {
                "id": "field5",
                "kind": "yes_no",
                "title": "Would you recommend us?",
                "validations": {
                    "required": True
                }
            },
            {
                "id": "field6",
                "kind": "long_text",
                "title": "Additional comments",
                "description": "Please share any additional feedback",
                "validations": {
                    "required": False,
                    "maxLength": 500
                },
                "properties": {
                    "placeholder": "Your feedback..."
                }
            },
            {
                "id": "field7",
                "kind": "phone_number",
                "title": "Your phone number",
                "validations": {
                    "required": False
                },
                "properties": {
                    "defaultCountryCode": "+1"
                }
            },
            {
                "id": "field8",
                "kind": "date",
                "title": "Date of visit",
                "validations": {
                    "required": False
                },
                "properties": {
                    "format": "YYYY-MM-DD"
                }
            }
        ],
        "hiddenFields": [],
        "logics": [],
        "variables": [],
        "translations": {},
        "fieldsUpdatedAt": int(time.time() * 1000),
        "suspended": False,
        "version": 2
    }


def test_validation():
    """Test field validation"""
    print("Testing Field Validation")
    print("=" * 50)
    
    client = MobileAPIClient(debug=False)
    form = create_test_form_data()
    
    # Test valid answers
    print("\n1. Testing valid answers...")
    valid_answers = {
        "field1": "John Doe",
        "field2": "john@example.com",
        "field3": {"value": ["choice1"]},
        "field4": 8,
        "field5": True,
        "field6": "Great service!",
        "field7": "+12125551234",
        "field8": "2024-01-15"
    }
    
    try:
        validated = client.validate_answers(form, valid_answers)
        print("✓ Valid answers passed validation")
    except ValidationError as e:
        print(f"✗ Unexpected validation error: {e}")
    
    # Test invalid email
    print("\n2. Testing invalid email...")
    invalid_email = valid_answers.copy()
    invalid_email["field2"] = "not-an-email"
    
    try:
        client.validate_answers(form, invalid_email)
        print("✗ Invalid email should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught invalid email: {e}")
    
    # Test missing required field
    print("\n3. Testing missing required field...")
    missing_required = valid_answers.copy()
    del missing_required["field1"]
    
    try:
        client.validate_answers(form, missing_required)
        print("✗ Missing required field should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught missing required field: {e}")
    
    # Test text too long
    print("\n4. Testing text exceeding max length...")
    too_long = valid_answers.copy()
    too_long["field1"] = "x" * 101  # Max is 100
    
    try:
        client.validate_answers(form, too_long)
        print("✗ Text too long should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught text too long: {e}")
    
    # Test invalid choice
    print("\n5. Testing invalid choice selection...")
    invalid_choice = valid_answers.copy()
    invalid_choice["field3"] = {"value": ["invalid_choice"]}
    
    try:
        client.validate_answers(form, invalid_choice)
        print("✗ Invalid choice should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught invalid choice: {e}")
    
    # Test multiple choices when not allowed
    print("\n6. Testing multiple choices when not allowed...")
    multiple_not_allowed = valid_answers.copy()
    multiple_not_allowed["field3"] = {"value": ["choice1", "choice2"]}
    
    try:
        client.validate_answers(form, multiple_not_allowed)
        print("✗ Multiple choices should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught multiple selection error: {e}")
    
    # Test rating out of range
    print("\n7. Testing rating out of range...")
    invalid_rating = valid_answers.copy()
    invalid_rating["field4"] = 11  # Max is 10
    
    try:
        client.validate_answers(form, invalid_rating)
        print("✗ Rating out of range should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught rating out of range: {e}")
    
    # Test phone without country code
    print("\n8. Testing phone without country code...")
    invalid_phone = valid_answers.copy()
    invalid_phone["field7"] = "2125551234"  # Missing +
    
    try:
        client.validate_answers(form, invalid_phone)
        print("✗ Phone without country code should have failed")
    except ValidationError as e:
        print(f"✓ Correctly caught invalid phone: {e}")
    
    # Test 'other' option in multiple choice
    print("\n9. Testing 'other' option in multiple choice...")
    with_other = valid_answers.copy()
    with_other["field3"] = {
        "value": [],
        "other": "My custom response"
    }
    
    try:
        validated = client.validate_answers(form, with_other)
        print("✓ 'Other' option passed validation")
    except ValidationError as e:
        print(f"✗ Unexpected validation error with 'other': {e}")


def test_answer_building():
    """Test building answers from user input"""
    print("\n\nTesting Answer Building")
    print("=" * 50)
    
    client = MobileAPIClient(debug=False)
    form = create_test_form_data()
    
    # Test building from field titles
    print("\n1. Testing building from field titles...")
    user_input = {
        "What's your name?": "Jane Smith",
        "Your email address": "jane@example.com",
        "How satisfied are you?": "Very Satisfied",  # Should match by label
        "Rate our service": "9",
        "Would you recommend us?": "yes",
        "Additional comments": "Excellent experience!",
        "Your phone number": "2125551234",  # Should add country code
        "Date of visit": "2024-01-20"
    }
    
    try:
        answers = client.build_answers_from_input(form, user_input)
        print("✓ Successfully built answers from user input")
        
        # Verify choice was matched by label
        if answers["field3"]["value"] == ["choice1"]:
            print("✓ Correctly matched choice by label")
        else:
            print(f"✗ Choice matching failed: {answers['field3']}")
        
        # Verify rating was converted to number
        if answers["field4"] == 9:
            print("✓ Correctly converted rating to number")
        else:
            print(f"✗ Rating conversion failed: {answers['field4']}")
        
        # Verify boolean conversion
        if answers["field5"] == True:
            print("✓ Correctly converted yes to boolean")
        else:
            print(f"✗ Boolean conversion failed: {answers['field5']}")
            
    except Exception as e:
        print(f"✗ Failed to build answers: {e}")
    
    # Test building from field IDs
    print("\n2. Testing building from field IDs...")
    id_input = {
        "field1": "Bob Johnson",
        "field2": "bob@example.com",
        "field3": "choice2",  # Direct choice ID
        "field4": 7,
        "field5": False,
        "field6": "Good service"
    }
    
    try:
        answers = client.build_answers_from_input(form, id_input)
        print("✓ Successfully built answers from field IDs")
    except Exception as e:
        print(f"✗ Failed to build answers: {e}")


def test_cli_functionality():
    """Test CLI functionality with real server"""
    print("\n\nTesting CLI Functionality")
    print("=" * 50)
    print("\nNOTE: This test requires a running server at http://localhost:9157")
    print("and a valid form ID to test against.\n")
    
    # Create test data files
    test_answers = {
        "answers": {
            "field1": "CLI Test User",
            "field2": "test@example.com",
            "field3": {"value": ["choice1"]},
            "field4": 8,
            "field5": True,
            "field6": "Testing from CLI"
        }
    }
    
    with open('test_answers.json', 'w') as f:
        json.dump(test_answers, f, indent=2)
    
    batch_data = {
        "form_id": "test-form-123",
        "submissions": [
            {
                "answers": {
                    "field1": "Batch User 1",
                    "field2": "batch1@example.com",
                    "field3": {"value": ["choice1"]},
                    "field4": 7,
                    "field5": True
                }
            },
            {
                "answers": {
                    "field1": "Batch User 2",
                    "field2": "batch2@example.com",
                    "field3": {"value": ["choice2"]},
                    "field4": 9,
                    "field5": True
                }
            }
        ]
    }
    
    with open('test_batch.json', 'w') as f:
        json.dump(batch_data, f, indent=2)
    
    print("✓ Created test data files:")
    print("  - test_answers.json")
    print("  - test_batch.json")
    print("\nYou can test the CLI with:")
    print("  python mobile_form_cli.py get-form <form-id>")
    print("  python mobile_form_cli.py validate <form-id> -a test_answers.json")
    print("  python mobile_form_cli.py submit <form-id> -a test_answers.json")
    print("  python mobile_form_cli.py batch -i test_batch.json")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Mobile API Client Test Suite")
    print("=" * 60)
    
    test_validation()
    test_answer_building()
    test_cli_functionality()
    
    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()