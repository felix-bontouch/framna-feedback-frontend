#!/usr/bin/env python3
"""Example usage of the Mobile API Client"""

from mobile_api_client import MobileAPIClient
from exceptions import ValidationError, MobileAPIError
import json


def example_basic_submission():
    """Example of basic form submission"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Form Submission")
    print("=" * 60)
    
    # Initialize client
    client = MobileAPIClient(
        base_url="http://localhost:9157",
        debug=True
    )
    
    # Replace with your actual form ID
    form_id = "test-form-123"
    
    try:
        # Fetch form structure
        form = client.get_form(form_id)
        print(f"\nForm: {form['name']}")
        print(f"Fields: {len(form.get('fields', []))}")
        
        # Build answers
        answers = {
            "field1": "John Doe",  # short_text
            "field2": {"value": ["choice1"]},  # multiple_choice (single)
            "field3": 8,  # rating
            "field4": True,  # yes_no
            "field5": "john.doe@example.com",  # email
        }
        
        # Validate answers
        validated_answers = client.validate_answers(form, answers)
        
        # Submit form
        result = client.submit_form(form_id, validated_answers)
        print(f"\nSubmission successful!")
        print(f"Submission ID: {result['submissionId']}")
        
    except ValidationError as e:
        print(f"\nValidation error: {e}")
        if e.field_title:
            print(f"Field: {e.field_title}")
        if e.value:
            print(f"Value provided: {e.value}")
    except MobileAPIError as e:
        print(f"\nAPI error: {e}")


def example_multiple_choice_with_other():
    """Example of multiple choice field with 'other' option"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multiple Choice with Other Option")
    print("=" * 60)
    
    client = MobileAPIClient(base_url="http://localhost:9157")
    form_id = "test-form-123"
    
    try:
        form = client.get_form(form_id)
        
        # Multiple choice with single selection
        single_choice = {"value": ["choice1"]}
        
        # Multiple choice with multiple selections
        multiple_choices = {"value": ["choice1", "choice2", "choice3"]}
        
        # Multiple choice with 'other' option
        choice_with_other = {
            "value": ["choice1"],
            "other": "My custom answer"
        }
        
        # Only 'other' selected
        only_other = {
            "value": [],
            "other": "Completely custom answer"
        }
        
        answers = {
            "multipleChoiceField1": single_choice,
            "multipleChoiceField2": multiple_choices,
            "multipleChoiceField3": choice_with_other,
            "multipleChoiceField4": only_other
        }
        
        validated = client.validate_answers(form, answers)
        result = client.submit_form(form_id, validated)
        print(f"Submission successful: {result['submissionId']}")
        
    except MobileAPIError as e:
        print(f"Error: {e}")


def example_complex_fields():
    """Example of complex field types"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Complex Field Types")
    print("=" * 60)
    
    client = MobileAPIClient(base_url="http://localhost:9157")
    form_id = "test-form-123"
    
    try:
        form = client.get_form(form_id)
        
        answers = {
            # Address field
            "addressField": {
                "address1": "123 Main Street",
                "address2": "Apt 4B",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "US"
            },
            
            # Full name field
            "fullNameField": {
                "firstName": "John",
                "lastName": "Doe"
            },
            
            # Phone number field (with country code)
            "phoneField": "+12125551234",
            
            # Date field
            "dateField": "2024-01-15",
            
            # Date range field
            "dateRangeField": {
                "start": "2024-01-01",
                "end": "2024-01-31"
            },
            
            # File upload field
            "fileField": {
                "url": "https://example.com/document.pdf",
                "name": "document.pdf",
                "size": 1024000,
                "type": "application/pdf"
            },
            
            # Country field (ISO code)
            "countryField": "US",
            
            # Input table field
            "tableField": [
                {"column1": "Row 1 Col 1", "column2": "Row 1 Col 2"},
                {"column1": "Row 2 Col 1", "column2": "Row 2 Col 2"}
            ]
        }
        
        validated = client.validate_answers(form, answers)
        result = client.submit_form(form_id, validated)
        print(f"Submission successful: {result['submissionId']}")
        
    except MobileAPIError as e:
        print(f"Error: {e}")


def example_build_answers_from_input():
    """Example of building answers from user-friendly input"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Build Answers from User Input")
    print("=" * 60)
    
    client = MobileAPIClient(base_url="http://localhost:9157")
    form_id = "test-form-123"
    
    try:
        form = client.get_form(form_id)
        
        # User-friendly input using field titles or IDs
        user_input = {
            "What's your name?": "John Doe",
            "How satisfied are you?": "Very Satisfied",  # Will match choice by label
            "Rate our service": "8",  # Will be converted to number
            "Would you recommend us?": "yes",  # Will be converted to boolean
            "Your email": "john@example.com",
            "Comments": "Great service, very happy!"
        }
        
        # Build and validate answers
        answers = client.build_answers_from_input(form, user_input)
        
        # Submit
        result = client.submit_form(form_id, answers)
        print(f"Submission successful: {result['submissionId']}")
        
    except MobileAPIError as e:
        print(f"Error: {e}")


def example_batch_submission():
    """Example of batch form submission"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Batch Submission")
    print("=" * 60)
    
    client = MobileAPIClient(base_url="http://localhost:9157")
    form_id = "test-form-123"
    
    # Multiple submissions
    submissions = [
        {
            "answers": {
                "field1": "User 1",
                "field2": {"value": ["choice1"]},
                "field3": 7
            }
        },
        {
            "answers": {
                "field1": "User 2",
                "field2": {"value": ["choice2"]},
                "field3": 9
            }
        },
        {
            "answers": {
                "field1": "User 3",
                "field2": {"value": ["choice3"]},
                "field3": 10
            }
        }
    ]
    
    try:
        results = client.batch_submit(form_id, submissions, delay=0.5)
        
        # Process results
        for result in results:
            if result['success']:
                print(f"✓ Submission {result['index']}: {result['result']['submissionId']}")
            else:
                print(f"✗ Submission {result['index']}: {result['error']}")
                
    except MobileAPIError as e:
        print(f"Error: {e}")


def example_interactive_submission():
    """Example of interactive form submission"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Interactive Submission")
    print("=" * 60)
    
    client = MobileAPIClient(base_url="http://localhost:9157")
    form_id = "test-form-123"
    
    try:
        # This will prompt the user for each field
        result = client.interactive_submit(form_id)
        if result:
            print(f"\nForm submitted successfully!")
            print(f"Submission ID: {result['submissionId']}")
    except MobileAPIError as e:
        print(f"Error: {e}")


def example_with_password_and_hidden_fields():
    """Example with password-protected form and hidden fields"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Password-Protected Form with Hidden Fields")
    print("=" * 60)
    
    client = MobileAPIClient(base_url="http://localhost:9157")
    form_id = "protected-form-123"
    
    try:
        form = client.get_form(form_id)
        
        answers = {
            "field1": "John Doe",
            "field2": {"value": ["choice1"]}
        }
        
        # Hidden fields for tracking
        hidden_fields = [
            {"id": "source", "value": "mobile_app"},
            {"id": "campaign", "value": "summer_2024"},
            {"id": "user_id", "value": "usr_12345"}
        ]
        
        validated = client.validate_answers(form, answers)
        
        result = client.submit_form(
            form_id=form_id,
            answers=validated,
            password="form_password_here",
            hidden_fields=hidden_fields,
            category="FEATURE"  # Categorize submission
        )
        
        print(f"Submission successful: {result['submissionId']}")
        
    except MobileAPIError as e:
        print(f"Error: {e}")


def example_load_from_json():
    """Example of loading submissions from JSON file"""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Load Submissions from JSON")
    print("=" * 60)
    
    # Create example JSON data
    json_data = {
        "form_id": "test-form-123",
        "submissions": [
            {
                "answers": {
                    "name": "Alice Smith",
                    "email": "alice@example.com",
                    "satisfaction": "Very Satisfied",
                    "rating": 9,
                    "comments": "Excellent service!"
                }
            },
            {
                "answers": {
                    "name": "Bob Johnson",
                    "email": "bob@example.com",
                    "satisfaction": "Satisfied",
                    "rating": 7,
                    "comments": "Good overall experience"
                }
            }
        ]
    }
    
    # Save to file
    with open('submissions.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    
    # Load and submit
    client = MobileAPIClient(base_url="http://localhost:9157")
    
    try:
        with open('submissions.json', 'r') as f:
            data = json.load(f)
        
        form_id = data['form_id']
        form = client.get_form(form_id)
        
        for submission in data['submissions']:
            # Build answers from user-friendly input
            answers = client.build_answers_from_input(form, submission['answers'])
            
            # Submit
            result = client.submit_form(form_id, answers)
            print(f"✓ Submitted: {result['submissionId']}")
            
    except MobileAPIError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("\nMobile API Client Examples\n")
    print("Select an example to run:")
    print("1. Basic form submission")
    print("2. Multiple choice with 'other' option")
    print("3. Complex field types")
    print("4. Build answers from user input")
    print("5. Batch submission")
    print("6. Interactive submission")
    print("7. Password-protected form")
    print("8. Load from JSON file")
    print("9. Run all examples")
    
    choice = input("\nEnter choice (1-9): ").strip()
    
    examples = {
        "1": example_basic_submission,
        "2": example_multiple_choice_with_other,
        "3": example_complex_fields,
        "4": example_build_answers_from_input,
        "5": example_batch_submission,
        "6": example_interactive_submission,
        "7": example_with_password_and_hidden_fields,
        "8": example_load_from_json,
    }
    
    if choice == "9":
        for func in examples.values():
            func()
    elif choice in examples:
        examples[choice]()
    else:
        print("Invalid choice")