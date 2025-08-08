# Mobile REST API Documentation

## Overview
The Mobile REST API provides a simplified, theme-free interface for mobile applications to interact with Framna Feedback forms. All visual and theme-related properties are automatically stripped, returning only functional data needed for form rendering and submission.

## Base URL
```
https://api.framna.com/api/mobile/forms
```

## Authentication
The mobile API endpoints are designed for public form access and do not require authentication. Forms must be active and not suspended to be accessible.

## Endpoints

### 1. Get Form Structure
Retrieve a mobile-optimized form structure without any visual/theme elements.

**Endpoint:** `GET /api/mobile/forms/:formId`

**Parameters:**
- `formId` (path parameter) - The ID of the form to retrieve

**Response:**
```json
{
  "id": "abc123",
  "teamId": "team123",
  "projectId": "proj456",
  "name": "Customer Feedback Survey",
  "description": "Help us improve our service",
  "interactiveMode": 1,
  "kind": 1,
  "settings": {
    "active": true,
    "captchaKind": "none",
    "requirePassword": false,
    "redirectOnCompletion": true,
    "redirectUrl": "https://example.com/thank-you",
    "filterSpam": true,
    "allowArchive": true,
    "locale": "en",
    "languages": ["en", "es"],
    "enableQuotaLimit": false,
    "quotaLimit": 0,
    "enableIpLimit": true,
    "ipLimitCount": 3
  },
  "fields": [
    {
      "id": "field1",
      "kind": "short_text",
      "title": "What's your name?",
      "description": "Please enter your full name",
      "validations": {
        "required": true,
        "minLength": 2,
        "maxLength": 100
      },
      "properties": {
        "placeholder": "John Doe"
      }
    },
    {
      "id": "field2",
      "kind": "multiple_choice",
      "title": "How satisfied are you?",
      "validations": {
        "required": true
      },
      "properties": {
        "choices": [
          {
            "id": "choice1",
            "label": "Very Satisfied",
            "score": 5
          },
          {
            "id": "choice2",
            "label": "Satisfied",
            "score": 4
          },
          {
            "id": "choice3",
            "label": "Neutral",
            "score": 3
          }
        ],
        "allowMultiple": false,
        "allowOther": true
      }
    }
  ],
  "hiddenFields": [],
  "logics": [],
  "variables": [],
  "translations": {},
  "fieldsUpdatedAt": 1703123456789,
  "suspended": false,
  "version": 2
}
```

**Error Responses:**
- `400 Bad Request` - Form is not active or suspended
- `404 Not Found` - Form does not exist

### 2. Get Specific Fields
Retrieve configuration for specific fields only (useful for progressive form loading).

**Endpoint:** `GET /api/mobile/forms/:formId/fields`

**Parameters:**
- `formId` (path parameter) - The ID of the form
- `fieldIds` (query parameter, optional) - Comma-separated list of field IDs to retrieve

**Example:**
```
GET /api/mobile/forms/abc123/fields?fieldIds=field1,field2,field3
```

**Response:**
```json
{
  "fields": [
    {
      "id": "field1",
      "kind": "short_text",
      "title": "What's your name?",
      "validations": {
        "required": true
      },
      "properties": {
        "placeholder": "Enter your name"
      }
    }
  ]
}
```

### 3. Submit Form
Submit form responses from a mobile application.

**Endpoint:** `POST /api/mobile/forms/:formId`

**Request Body:**
```json
{
  "answers": {
    "field1": "John Doe",
    "field2": {
      "value": ["choice1"]
    }
  },
  "startedAt": 1703123456789,
  "clientInfo": {
    "ip": "192.168.1.1",
    "userAgent": "MyApp/1.0 (iOS 16.0)",
    "os": "iOS",
    "osVersion": "16.0",
    "appVersion": "1.0.0",
    "device": "iPhone 14 Pro",
    "deviceId": "550e8400-e29b-41d4-a716-446655440000",
    "locale": "en-US"
  },
  "category": "GENERAL",
  "hiddenFields": [
    {
      "id": "source",
      "value": "mobile_app"
    }
  ],
  "password": "form_password",
  "captchaToken": "captcha_verification_token",
  "isPartial": false
}
```

**Category Options:**
- `NPS` - Net Promoter Score feedback
- `FEATURE` - About a specific feature
- `USER_FLOW` - Feedback on app flows and UX
- `PERFORMANCE` - Performance-related issues
- `GENERAL` - General feedback (default)
- `ONBOARDING` - Onboarding experience feedback
- `RATING` - App store rating prompts

**Response:**
```json
{
  "success": true,
  "submissionId": "sub123456",
  "timestamp": 1703123456789,
  "redirectUrl": "https://example.com/thank-you",
  "message": "Form submitted successfully"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid submission data, form constraints violated, or validation errors
- `404 Not Found` - Form does not exist

## Field Types
The mobile API supports all Framna field types without visual properties:
- `short_text` - Single line text input
- `long_text` - Multi-line text input
- `multiple_choice` - Radio buttons or checkboxes
- `dropdown` - Dropdown selection
- `email` - Email input with validation
- `phone_number` - Phone number with country code
- `number` - Numeric input
- `date` - Date picker
- `time` - Time picker
- `file_upload` - File upload
- `rating` - Star or numeric rating
- `scale` - Linear scale
- `matrix` - Table/grid questions
- `ranking` - Drag to rank items
- `picture_choice` - Image selection (URLs only)
- `yes_no` - Binary choice
- `legal` - Terms acceptance
- `signature` - Digital signature
- `payment` - Payment collection

## Answer Formats

**IMPORTANT:** Each field type requires a specific answer format. Incorrect formats will result in validation errors.

### Text Fields
**short_text, long_text, email, website**
```json
{
  "fieldId": "Simple text string"
}
```

### Multiple Choice / Picture Choice
**CRITICAL:** Multiple choice fields require an object with a `value` array, NOT a simple string.

**Single selection (allowMultiple: false):**
```json
{
  "fieldId": {
    "value": ["choiceId1"]
  }
}
```

**Multiple selection (allowMultiple: true):**
```json
{
  "fieldId": {
    "value": ["choiceId1", "choiceId2", "choiceId3"]
  }
}
```

**With "Other" option (allowOther: true):**
```json
{
  "fieldId": {
    "value": ["choiceId1"],
    "other": "Custom text entered by user"
  }
}
```

**Only "Other" selected:**
```json
{
  "fieldId": {
    "value": [],
    "other": "Custom text entered by user"
  }
}
```

### Yes/No
```json
{
  "fieldId": true  // or false
}
```

### Number
```json
{
  "fieldId": 42
}
```

### Rating / Opinion Scale
```json
{
  "fieldId": 5  // Number between 1 and total
}
```

### Date
```json
{
  "fieldId": "2024-01-15"  // Format depends on field.properties.format
}
```

### Date Range
```json
{
  "fieldId": {
    "start": "2024-01-15",
    "end": "2024-01-20"
  }
}
```

### Phone Number
```json
{
  "fieldId": "+1234567890"  // Include country code
}
```

### Full Name
```json
{
  "fieldId": {
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

### Address
```json
{
  "fieldId": {
    "address1": "123 Main St",
    "address2": "Apt 4B",  // Optional
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "US"
  }
}
```

### File Upload
```json
{
  "fieldId": {
    "url": "https://storage.example.com/file.pdf",
    "name": "document.pdf",
    "size": 1024000,
    "type": "application/pdf"
  }
}
```

### Legal Terms
```json
{
  "fieldId": true  // Must be true if required
}
```

### Input Table
```json
{
  "fieldId": [
    {
      "column1": "value1",
      "column2": "value2"
    },
    {
      "column1": "value3",
      "column2": "value4"
    }
  ]
}
```

### Signature
```json
{
  "fieldId": "data:image/png;base64,iVBORw0KGgoAAAANS..."  // Base64 encoded PNG
}
```

### Country
```json
{
  "fieldId": "US"  // ISO 3166-1 alpha-2 country code
}
```

## Common Validation Errors

When validation fails, the API returns detailed error information:

```json
{
  "statusCode": 400,
  "message": "Validation failed for field \"Field Title\": Error details",
  "error": "Bad Request",
  "field": "fieldId",
  "fieldTitle": "Field Title",
  "fieldKind": "multiple_choice"
}
```

### Common Errors:
1. **"This field is required"** - Required field is missing or has incorrect format
2. **"Multiple choose is not allowed"** - Sent multiple values when allowMultiple is false
3. **"Cannot select non-specified choices"** - Choice ID doesn't exist in field.properties.choices
4. **"Other value is not allowed"** - Sent "other" value when allowOther is false
5. **"The text length must be between X to Y"** - Text length validation failed
6. **"Please enter a valid email address"** - Email format validation failed

## Integration Example

### React Native
```javascript
import axios from 'axios';

const API_BASE = 'https://api.framna.com/api/mobile/forms';

// Fetch form structure
const getForm = async (formId) => {
  try {
    const response = await axios.get(`${API_BASE}/${formId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching form:', error.response?.data);
    throw error;
  }
};

// Submit form
const submitForm = async (formId, answers, category = 'GENERAL') => {
  try {
    // Example answers object with correct formats:
    // {
    //   "textField": "John Doe",
    //   "multipleChoiceField": { "value": ["choiceId1"] },
    //   "ratingField": 5,
    //   "dateField": "2024-01-15"
    // }
    const response = await axios.post(`${API_BASE}/${formId}`, {
      answers,
      startedAt: Date.now(),
      clientInfo: {
        ip: await getDeviceIP(),
        userAgent: getUserAgent(),
        os: Platform.OS,
        osVersion: Platform.Version,
        appVersion: getVersion(),
        device: getDeviceModel(),
        deviceId: getUniqueId(),
        locale: getLocale()
      },
      category
    });
    return response.data;
  } catch (error) {
    console.error('Error submitting form:', error.response?.data);
    throw error;
  }
};

// Example: Building answers for multiple choice fields
const buildMultipleChoiceAnswer = (selectedChoices, otherText = null) => {
  const answer = {
    value: selectedChoices // Array of choice IDs
  };
  if (otherText) {
    answer.other = otherText;
  }
  return answer;
};

// Usage example
const answers = {
  "field1": "John Doe", // Text field
  "field2": buildMultipleChoiceAnswer(["choice1"]), // Single choice
  "field3": buildMultipleChoiceAnswer(["choice1", "choice2"]), // Multiple choices
  "field4": buildMultipleChoiceAnswer(["choice1"], "Custom answer"), // With other
  "field5": 8, // Rating field
  "field6": true // Yes/No field
};
```

### Swift (iOS)
```swift
import Foundation

struct MobileFormAPI {
    static let baseURL = "https://api.framna.com/api/mobile/forms"
    
    static func getForm(formId: String) async throws -> FormResponse {
        let url = URL(string: "\(baseURL)/\(formId)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(FormResponse.self, from: data)
    }
    
    static func submitForm(formId: String, answers: [String: Any], category: String = "GENERAL") async throws -> SubmissionResponse {
        let url = URL(string: "\(baseURL)/\(formId)")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Example answers dictionary with correct formats:
        // let answers = [
        //     "textField": "John Doe",
        //     "multipleChoiceField": ["value": ["choiceId1"]],
        //     "ratingField": 5,
        //     "dateField": "2024-01-15"
        // ]
        
        let submission = [
            "answers": answers,
            "startedAt": Date().timeIntervalSince1970 * 1000,
            "clientInfo": [
                "ip": getDeviceIP(),
                "userAgent": getUserAgent(),
                "os": "iOS",
                "osVersion": UIDevice.current.systemVersion,
                "appVersion": Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0",
                "device": UIDevice.current.model,
                "deviceId": UIDevice.current.identifierForVendor?.uuidString ?? "",
                "locale": Locale.current.identifier
            ],
            "category": category
        ] as [String : Any]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: submission)
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(SubmissionResponse.self, from: data)
    }
    
    // Helper function to build multiple choice answers
    static func buildMultipleChoiceAnswer(selectedChoices: [String], otherText: String? = nil) -> [String: Any] {
        var answer: [String: Any] = ["value": selectedChoices]
        if let other = otherText {
            answer["other"] = other
        }
        return answer
    }
}

// Usage example
let answers: [String: Any] = [
    "field1": "John Doe", // Text field
    "field2": MobileFormAPI.buildMultipleChoiceAnswer(selectedChoices: ["choice1"]), // Single choice
    "field3": MobileFormAPI.buildMultipleChoiceAnswer(selectedChoices: ["choice1", "choice2"]), // Multiple choices
    "field4": MobileFormAPI.buildMultipleChoiceAnswer(selectedChoices: ["choice1"], otherText: "Custom answer"), // With other
    "field5": 8, // Rating field
    "field6": true // Yes/No field
]
```

## Best Practices

1. **Cache Form Structure**: Form structures change infrequently. Cache them locally to reduce API calls.

2. **Handle Offline Submissions**: Store submissions locally when offline and sync when connection is restored.

3. **Progressive Loading**: For large forms, use the fields endpoint to load fields as needed.

4. **Error Handling**: Always handle API errors gracefully and provide user-friendly messages.

5. **Client Information**: Always provide accurate client information for spam filtering and analytics.

6. **Validation**: Perform client-side validation before submission to improve user experience.

## Rate Limiting
The API implements rate limiting to prevent abuse:
- 1000 requests per minute per IP
- 100 form submissions per hour per IP

## Support
For API support and questions, please contact support@framna.com or visit our developer documentation at https://docs.framna.com/api/mobile