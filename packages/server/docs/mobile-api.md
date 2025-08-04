# Mobile API Documentation

## Overview

The Framna Feedback server now supports a mobile-optimized API that returns simplified form data without visual/theme elements. This is achieved through a platform detection mechanism in the existing GraphQL endpoints.

## Usage

### GraphQL Query

To fetch form data optimized for mobile consumption, add the `platform: "mobile"` parameter to your GraphQL query:

```graphql
query GetMobileForm($formId: String!, $platform: String) {
  publicForm(input: { formId: $formId, platform: $platform }) {
    id
    teamId
    projectId
    memberId
    name
    description
    interactiveMode
    kind
    settings {
      active
      enableProgress
      enableQuestionList
      requirePassword
      locale
      languages
      # ... other functional settings
    }
    fields {
      id
      kind
      title
      description
      validations
      properties
      width
      hide
      frozen
    }
    hiddenFields
    logics
    variables
    translations
    version
    status
  }
}
```

### Example Request

```javascript
const response = await fetch('https://your-server.com/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: MOBILE_FORM_QUERY,
    variables: {
      formId: 'your-form-id',
      platform: 'mobile'  // This triggers mobile optimization
    }
  })
});
```

## What Gets Stripped Out

When `platform: "mobile"` is specified, the following visual/theme elements are removed:

### Removed from Form Response:
- `themeSettings` (logo, theme colors, fonts, custom CSS)
- `customReport` theme data
- Integration tracking codes (Google Analytics, Facebook Pixel)

### Removed from Field Properties:
- Visual styling properties (colors, images)
- Layout-specific properties
- Animation settings
- Background images
- Custom CSS classes

### Removed from Choice Properties:
- `image` (choice images)
- `color` (choice colors)

## What Is Preserved

All functional data needed for form logic and validation is preserved:

### Form Data:
- All form metadata (id, name, description, etc.)
- Form settings (validation rules, limits, localization)
- Form logic and conditional visibility rules
- Variables and calculations
- Translations for multi-language support

### Field Data:
- Field definitions and types
- Validation rules
- Functional properties (placeholders, default values, etc.)
- Choice labels and values
- Scoring information
- Field dependencies

## Mobile Client Implementation

Mobile clients should:

1. Always specify `platform: "mobile"` when fetching forms
2. Implement their own native UI components for each field type
3. Apply their own styling and themes
4. Handle form logic and validation using the provided rules

## Benefits

1. **Reduced Payload Size**: Mobile responses are significantly smaller
2. **Native UI Freedom**: Mobile apps can implement platform-specific UI
3. **Backward Compatible**: Existing web clients continue to work unchanged
4. **Single API**: No need for separate mobile endpoints

## Example Response Comparison

### Web Response (Default):
```json
{
  "id": "form_123",
  "fields": [...],
  "themeSettings": {
    "logo": "https://...",
    "theme": {
      "fontFamily": "Inter",
      "backgroundColor": "#ffffff",
      "buttonBackground": "#3b82f6",
      "customCSS": "..."
    }
  }
}
```

### Mobile Response:
```json
{
  "id": "form_123",
  "fields": [
    {
      "id": "field_1",
      "kind": "SHORT_TEXT",
      "title": "What's your name?",
      "validations": { "required": true },
      "properties": { "placeholder": "Enter your name" }
    }
  ],
  "settings": {
    "active": true,
    "enableProgress": true
  }
  // Note: No themeSettings or visual properties
}
```