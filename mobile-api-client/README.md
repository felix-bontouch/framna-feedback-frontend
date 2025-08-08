# Mobile API Client for Framna Feedback

A Python client library for interacting with the Framna Feedback Mobile REST API. This client provides a simple and robust way to fetch forms and submit responses programmatically.

## Features

- 🚀 **Complete API Coverage**: Fetch forms, get specific fields, submit responses
- ✅ **Built-in Validation**: Validate answers before submission with detailed error messages
- 🔄 **Dynamic Field Handling**: Automatic handling of all 20+ field types
- 📦 **Batch Processing**: Submit multiple responses efficiently
- 🎯 **Interactive Mode**: CLI interface for interactive form submission
- 🛡️ **Error Handling**: Comprehensive error handling with custom exceptions
- 💾 **Caching**: Optional form caching to reduce API calls
- 🔧 **CLI Tool**: Command-line interface for all operations

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd mobile-api-client

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from mobile_api_client import MobileAPIClient

# Initialize client
client = MobileAPIClient(base_url="http://localhost:9157")

# Fetch form
form = client.get_form("form-id-123")

# Submit form with answers
answers = {
    "field1": "John Doe",
    "field2": {"value": ["choice1"]},  # Multiple choice
    "field3": 8,  # Rating
    "field4": True,  # Yes/No
    "field5": "john@example.com"  # Email
}

# Validate and submit
validated = client.validate_answers(form, answers)
result = client.submit_form("form-id-123", validated)
print(f"Submission ID: {result['submissionId']}")
```

### Command Line Interface

```bash
# Get form structure
python mobile_form_cli.py get-form form-id-123

# Submit form with answers from JSON
python mobile_form_cli.py submit form-id-123 -a answers.json

# Interactive submission
python mobile_form_cli.py interactive form-id-123

# Batch submission
python mobile_form_cli.py batch -i submissions.json

# Validate without submitting
python mobile_form_cli.py validate form-id-123 -a answers.json
```

## Field Types Support

The client automatically handles all Framna field types:

### Text Fields
- `short_text` - Single line text
- `long_text` - Multi-line text
- `email` - Email with validation
- `website` - URL with validation

### Choice Fields
- `multiple_choice` - Radio/checkbox with optional "other"
- `dropdown` - Dropdown selection
- `picture_choice` - Image selection

### Boolean Fields
- `yes_no` - Binary choice
- `legal` - Terms acceptance

### Numeric Fields
- `number` - Numeric input
- `rating` - Star rating (1-N)
- `opinion_scale` - Linear scale

### Date/Time Fields
- `date` - Date picker
- `date_range` - Start and end dates
- `time` - Time picker

### Complex Fields
- `phone_number` - With country code
- `address` - Full address with components
- `full_name` - First and last name
- `country` - ISO country code
- `file_upload` - File metadata
- `signature` - Base64 encoded image
- `input_table` - Tabular data
- `matrix` - Grid questions

## Answer Formats

### Multiple Choice Fields

```python
# Single selection
{"value": ["choice1"]}

# Multiple selections
{"value": ["choice1", "choice2", "choice3"]}

# With "other" option
{"value": ["choice1"], "other": "Custom text"}

# Only "other" selected
{"value": [], "other": "Custom text"}
```

### Complex Fields

```python
# Address
{
    "address1": "123 Main St",
    "address2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "US"
}

# Full Name
{
    "firstName": "John",
    "lastName": "Doe"
}

# Date Range
{
    "start": "2024-01-01",
    "end": "2024-01-31"
}
```

## Advanced Features

### Batch Submission

```python
submissions = [
    {"answers": {"field1": "User 1", "field2": {"value": ["choice1"]}}},
    {"answers": {"field1": "User 2", "field2": {"value": ["choice2"]}}},
]

results = client.batch_submit("form-id", submissions, delay=0.5)
```

### Interactive Mode

```python
# Prompts user for each field
result = client.interactive_submit("form-id")
```

### Build Answers from User Input

```python
# Use field titles instead of IDs
user_input = {
    "What's your name?": "John Doe",
    "How satisfied are you?": "Very Satisfied",  # Matches by label
    "Rate our service": "8",  # Converts to number
}

answers = client.build_answers_from_input(form, user_input)
```

### Password-Protected Forms

```python
result = client.submit_form(
    form_id="protected-form",
    answers=answers,
    password="form_password"
)
```

### Hidden Fields

```python
hidden_fields = [
    {"id": "source", "value": "mobile_app"},
    {"id": "campaign", "value": "summer_2024"}
]

result = client.submit_form(
    form_id="form-id",
    answers=answers,
    hidden_fields=hidden_fields
)
```

## Error Handling

The client provides detailed error messages for validation failures:

```python
try:
    result = client.submit_form(form_id, answers)
except ValidationError as e:
    print(f"Field: {e.field_title}")
    print(f"Error: {e.message}")
    print(f"Value provided: {e.value}")
except FormNotFoundError as e:
    print(f"Form not found: {e.form_id}")
except FormInactiveError as e:
    print(f"Form inactive: {e.reason}")
```

## Configuration

```python
client = MobileAPIClient(
    base_url="http://localhost:9157",
    timeout=30,  # Request timeout in seconds
    retry_attempts=3,  # Number of retries
    verify_ssl=True,  # SSL verification
    debug=True,  # Enable debug output
    cache_forms=True,  # Cache form structures
    cache_ttl=300  # Cache TTL in seconds
)
```

## Testing

Run the test suite:

```bash
# Run validation tests
python test_mobile_form_cli.py

# Test with example scripts
python example_usage.py
```

## JSON File Formats

### Answers File (answers.json)

```json
{
  "answers": {
    "field1": "John Doe",
    "field2": {"value": ["choice1"]},
    "field3": 8,
    "field4": true,
    "field5": "john@example.com"
  },
  "password": "optional_password",
  "category": "GENERAL",
  "hiddenFields": [
    {"id": "source", "value": "mobile"}
  ]
}
```

### Batch Submissions (submissions.json)

```json
{
  "form_id": "form-123",
  "submissions": [
    {
      "answers": {
        "field1": "User 1",
        "field2": {"value": ["choice1"]}
      }
    },
    {
      "answers": {
        "field1": "User 2",
        "field2": {"value": ["choice2"]}
      }
    }
  ]
}
```

## API Endpoints

The client interacts with these Mobile API endpoints:

- `GET /api/mobile/forms/:formId` - Get form structure
- `GET /api/mobile/forms/:formId/fields` - Get specific fields
- `POST /api/mobile/forms/:formId` - Submit form

## Requirements

- Python 3.7+
- requests >= 2.28.0
- urllib3 >= 1.26.0
- python-dateutil >= 2.8.0

## License

MIT

## Support

For issues or questions, please contact the Framna Feedback team.