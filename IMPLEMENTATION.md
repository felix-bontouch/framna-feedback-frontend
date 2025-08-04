# IMPLEMENTATION.md - Framna Feedback API-First Migration Guide

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Architecture Analysis](#current-architecture-analysis)
3. [Target Architecture](#target-architecture)
4. [Migration Phases](#migration-phases)
5. [Technical Specifications](#technical-specifications)
6. [API Design](#api-design)
7. [Risk Assessment](#risk-assessment)
8. [Testing Strategy](#testing-strategy)
9. [Implementation Checklist](#implementation-checklist)

## Executive Summary

This document provides a comprehensive guide for transforming Framna Feedback from a web-based form rendering platform into an API-first service that enables mobile applications to fetch form definitions and submit responses using native UI components.

### Key Objectives

1. **Maintain Form Builder & Analytics**: Keep the web interface for creating and managing forms and their submission
2. **Remove Visual Elements**: Eliminate styling/theming in favor of content and logic
3. **API-First Design**: Create robust APIs for mobile consumption
4. **Remove Payments**: Completely remove Stripe and payment functionality
5. **Extract Business Logic**: Separate logic from UI components

### Scope

- **In Scope**: Form creation, logic, validation, submission handling, API design
- **Out of Scope**: Visual theming, payment processing, web-based form rendering for end-users

## Current Architecture Analysis

### Package Structure

```
frontend/
├── packages/
│   ├── webapp/          # React admin interface (KEEP & SIMPLIFY)
│   ├── server/          # NestJS backend (ENHANCE)
│   ├── form-renderer/   # React form components (REFACTOR)
│   ├── answer-utils/    # Answer processing (EXTRACT LOGIC)
│   ├── shared-types-enums/ # Type definitions (ENHANCE)
│   └── utils/           # Common utilities (KEEP)
```

### Current Dependencies

#### UI Dependencies to Remove
- `@radix-ui/*` - UI component library
- `tailwindcss` - CSS framework
- `@tabler/icons-react` - Icon library
- `react-transition-state` - Animation library
- `flag-icons` - Country flag icons
- CSS/SCSS files for styling

#### Payment Dependencies to Remove
- `stripe` - Payment processing
- All Stripe-related type definitions
- Payment webhook handlers

### Data Flow Analysis

```
Current Flow:
User → Web Form → React Renderer → GraphQL → Backend → Database

Target Flow:
Mobile App → REST/GraphQL API → Backend Logic → Database
Admin → Web UI → GraphQL → Backend → Database
```

### Field Types Inventory

The system supports 30+ field types that must be preserved:

```typescript
// Core Input Fields
SHORT_TEXT, LONG_TEXT, NUMBER, EMAIL, URL, PHONE_NUMBER

// Choice Fields  
YES_NO, MULTIPLE_CHOICE, PICTURE_CHOICE, RATING, OPINION_SCALE

// Date/Time Fields
DATE, DATE_RANGE, TIME

// Complex Fields
ADDRESS, FULL_NAME, COUNTRY, FILE_UPLOAD, SIGNATURE, INPUT_TABLE

// Statement Fields
WELCOME, THANK_YOU, STATEMENT, LEGAL_TERMS

// System Fields
HIDDEN_FIELDS, VARIABLE, SUBMIT_DATE
```

## Target Architecture

### System Components

```
┌─────────────────┐     ┌──────────────────┐
│  Mobile Apps    │     │  Web Admin UI    │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│          API Gateway (NestJS)           │
├─────────────────────────────────────────┤
│  • REST Endpoints for Mobile            │
│  • GraphQL for Admin UI                 │
│  • Authentication & Authorization       │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │  Core Logic    │
         │   Package      │
         └───────┬────────┘
                 │
    ┌────────────▼────────────┐
    │   Data Layer            │
    │  (MongoDB + Redis)      │
    └─────────────────────────┘
```

### Package Restructuring

```
frontend/
├── packages/
│   ├── webapp/              # Simplified admin UI
│   ├── server/              # Enhanced API server
│   ├── form-logic/          # NEW: Pure logic package
│   ├── mobile-api/          # NEW: Mobile API types
│   ├── answer-utils/        # Refactored without HTML
│   ├── shared-types-enums/  # Enhanced types
│   └── utils/               # Common utilities
```

## Migration Phases

### Phase 1: Payment Removal (Week 1-2) ✅ COMPLETED

✅ **Completed Tasks:**
1. Removed PAYMENT enum from FieldKindEnum
2. Deleted all payment-related types and interfaces (NumberPrice, VariablePrice, ServerSidePaymentValue, ClientSidePaymentValue)
3. Removed stripeAccount from FormModel
4. Deleted backend payment services, resolvers, and controllers
5. Removed frontend payment components and services
6. Cleaned up form renderer payment support
7. Removed Stripe dependencies from package.json files
8. Created and ran database migration to remove payment fields
9. Verified complete removal with verification script

**Files Modified:** 40+ files across all packages
**Files Deleted:** 15 payment-specific files
**Dependencies Removed:** stripe, @types/stripe-v3

### Phase 2: UI Simplification (Week 3-4)

#### 2.1 Form Builder Changes

Remove these UI elements from webapp:
- Theme customization panel
- Font selection
- Color pickers (except for functional uses)
- Background image uploads
- Custom CSS editor
- Animation settings

Keep these functional elements:
- Field configuration
- Logic builder
- Validation rules
- Field ordering
- Conditional visibility

#### 2.2 Component Simplification

```typescript
// Before: Complex themed component
<FormField
  theme={theme}
  fontFamily="Inter"
  fontSize="large"
  backgroundColor="#f0f0f0"
  textColor="#333"
  borderRadius={8}
  animate={true}
/>

// After: Simple functional component
<FormField
  type={field.type}
  validations={field.validations}
  logic={field.logic}
/>
```

### Phase 3: API Development (Week 5-6)

#### 3.1 REST Endpoint Structure

```typescript
// Form Definition Endpoints
GET    /api/v1/forms/:formId
GET    /api/v1/forms/:formId/fields
GET    /api/v1/forms/:formId/logic
POST   /api/v1/forms/:formId/validate

// Submission Endpoints
POST   /api/v1/submissions/start
PUT    /api/v1/submissions/:sessionId
POST   /api/v1/submissions/:sessionId/complete
GET    /api/v1/submissions/:sessionId/status

// File Handling
POST   /api/v1/files/upload-url
POST   /api/v1/files/signature
DELETE /api/v1/files/:fileId
```

#### 3.2 GraphQL Schema Updates

```graphql
# Remove payment types
type Form {
  id: ID!
  fields: [Field!]!
  # stripeAccount: StripeAccount @deprecated(reason: "Payments removed")
}

# Add mobile-specific queries
extend type Query {
  mobileForm(id: ID!): MobileFormResponse!
  validateField(formId: ID!, fieldId: ID!, value: JSON!): ValidationResult!
}

type MobileFormResponse {
  id: ID!
  version: String!
  fields: [MobileField!]!
  logic: [LogicRule!]!
  settings: FormSettings!
}
```

### Phase 4: Logic Extraction (Week 7-8)

#### 4.1 New Logic Package Structure

```
packages/form-logic/
├── src/
│   ├── validation/
│   │   ├── rules/
│   │   ├── validator.ts
│   │   └── index.ts
│   ├── logic/
│   │   ├── conditions.ts
│   │   ├── actions.ts
│   │   └── processor.ts
│   ├── calculator/
│   │   ├── variables.ts
│   │   └── expressions.ts
│   └── index.ts
├── tests/
└── package.json
```

#### 4.2 Validation Engine Refactor

```typescript
// Pure validation logic without UI dependencies
export class FieldValidator {
  static validate(
    field: FormField,
    value: any,
    context?: ValidationContext
  ): ValidationResult {
    const errors: ValidationError[] = [];
    
    // Required validation
    if (field.validations?.required && !value) {
      errors.push({
        code: 'REQUIRED',
        message: 'This field is required'
      });
    }
    
    // Type-specific validation
    switch (field.kind) {
      case FieldKindEnum.EMAIL:
        if (value && !isValidEmail(value)) {
          errors.push({
            code: 'INVALID_EMAIL',
            message: 'Please enter a valid email'
          });
        }
        break;
      // ... other field types
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
}
```

### Phase 5: Mobile API Implementation (Week 9-10)

#### 5.1 API Response Models

```typescript
// Mobile-optimized form response
export interface MobileFormDTO {
  id: string;
  version: string;
  title: string;
  description?: string;
  fields: MobileFieldDTO[];
  logic: LogicRuleDTO[];
  settings: {
    multiPage: boolean;
    showProgress: boolean;
    allowPartialSubmit: boolean;
  };
}

export interface MobileFieldDTO {
  id: string;
  type: FieldType;
  title: string;
  description?: string;
  required: boolean;
  validations?: ValidationRule[];
  properties: Record<string, any>;
  conditions?: VisibilityCondition[];
}

// Submission session
export interface SubmissionSessionDTO {
  sessionId: string;
  formId: string;
  formVersion: string;
  answers: Record<string, any>;
  currentFieldId?: string;
  completedFields: string[];
  createdAt: Date;
  expiresAt: Date;
}
```

#### 5.2 Session Management

```typescript
@Injectable()
export class MobileSubmissionService {
  async createSession(formId: string): Promise<SubmissionSessionDTO> {
    const form = await this.formService.findById(formId);
    if (!form || !form.settings.active) {
      throw new BadRequestException('Form not available');
    }
    
    const session = {
      sessionId: nanoid(),
      formId,
      formVersion: form.version,
      answers: {},
      completedFields: [],
      createdAt: new Date(),
      expiresAt: addHours(new Date(), 24)
    };
    
    await this.redis.setex(
      `session:${session.sessionId}`,
      86400, // 24 hours
      JSON.stringify(session)
    );
    
    return session;
  }
  
  async updateSession(
    sessionId: string, 
    updates: Partial<SubmissionSessionDTO>
  ): Promise<void> {
    const session = await this.getSession(sessionId);
    if (!session) {
      throw new NotFoundException('Session not found');
    }
    
    const updated = { ...session, ...updates };
    await this.redis.setex(
      `session:${sessionId}`,
      86400,
      JSON.stringify(updated)
    );
  }
}
```

## Technical Specifications

### API Authentication

```typescript
// JWT-based authentication for mobile
export interface MobileAuthToken {
  iss: 'framna-mobile-api';
  sub: string; // Anonymous or user ID
  formId: string;
  sessionId?: string;
  iat: number;
  exp: number;
}

// Token generation
function generateMobileToken(formId: string): string {
  return jwt.sign(
    {
      iss: 'framna-mobile-api',
      sub: 'anonymous',
      formId,
      iat: Date.now() / 1000,
      exp: Date.now() / 1000 + 86400 // 24 hours
    },
    JWT_SECRET
  );
}
```

### File Upload Flow

```typescript
// 1. Request upload URL
POST /api/v1/files/upload-url
{
  "formId": "...",
  "fieldId": "...",
  "filename": "document.pdf",
  "contentType": "application/pdf",
  "size": 1048576
}

// Response
{
  "uploadUrl": "https://s3.amazon.com/...",
  "fileId": "file_xyz123",
  "expiresAt": "2024-01-01T00:00:00Z"
}

// 2. Mobile app uploads directly to S3
PUT <uploadUrl>
Content-Type: application/pdf
[Binary data]

// 3. Confirm upload
POST /api/v1/files/confirm
{
  "fileId": "file_xyz123"
}
```

### Error Response Standard

```typescript
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
    timestamp: string;
    path: string;
  };
}

// Field validation errors
export interface ValidationError {
  error: {
    code: 'VALIDATION_ERROR';
    message: 'Validation failed';
    details: {
      fields: {
        [fieldId: string]: {
          code: string;
          message: string;
        }[];
      };
    };
  };
}
```

## API Design

### RESTful Endpoints

#### Form Retrieval

```http
GET /api/v1/forms/:formId
Authorization: Bearer <token>

Response 200:
{
  "data": {
    "id": "form_123",
    "version": "1.0.0",
    "title": "Customer Feedback",
    "description": "Help us improve",
    "fields": [...],
    "logic": [...],
    "settings": {...}
  }
}
```

#### Start Submission

```http
POST /api/v1/submissions/start
Authorization: Bearer <token>
Content-Type: application/json

{
  "formId": "form_123",
  "metadata": {
    "source": "ios-app",
    "version": "1.0.0"
  }
}

Response 201:
{
  "data": {
    "sessionId": "sess_xyz789",
    "formId": "form_123",
    "expiresAt": "2024-01-01T00:00:00Z"
  }
}
```

#### Update Answers

```http
PUT /api/v1/submissions/:sessionId
Authorization: Bearer <token>
Content-Type: application/json

{
  "answers": {
    "field_1": "John Doe",
    "field_2": "john@example.com",
    "field_3": ["option_1", "option_2"]
  },
  "currentFieldId": "field_3"
}

Response 200:
{
  "data": {
    "sessionId": "sess_xyz789",
    "validationResults": {
      "field_1": { "valid": true },
      "field_2": { "valid": true },
      "field_3": { "valid": true }
    },
    "progress": {
      "completed": 3,
      "total": 10,
      "percentage": 30
    }
  }
}
```

### GraphQL Operations

```graphql
# Mobile-specific queries
query GetMobileForm($id: ID!) {
  mobileForm(id: $id) {
    id
    version
    fields {
      id
      type
      title
      description
      required
      validations {
        rule
        value
        message
      }
      properties
    }
    logic {
      id
      conditions {
        fieldId
        operator
        value
      }
      actions {
        type
        target
        value
      }
    }
  }
}

mutation StartMobileSubmission($formId: ID!) {
  startSubmission(formId: $formId) {
    sessionId
    expiresAt
  }
}

mutation UpdateSubmissionAnswers(
  $sessionId: ID!
  $answers: JSON!
) {
  updateAnswers(
    sessionId: $sessionId
    answers: $answers
  ) {
    validationResults
    progress {
      completed
      total
    }
  }
}
```

## Risk Assessment

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Breaking existing forms | High | Medium | Comprehensive migration scripts and testing |
| API performance issues | High | Low | Caching, pagination, field lazy-loading |
| Data loss during migration | Critical | Low | Backups, staged rollout, rollback plan |
| Mobile app compatibility | Medium | Medium | Versioned API, deprecation notices |

### Business Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| User confusion | Medium | High | Clear documentation, migration guides |
| Feature parity gaps | Medium | Medium | Phased approach, feature flags |
| Integration disruption | High | Low | Parallel running, gradual cutover |

### Security Considerations

1. **Authentication**: JWT tokens with form-specific scopes
2. **Rate Limiting**: Implement per-IP and per-token limits
3. **Input Validation**: Strict validation on all endpoints
4. **File Upload**: Size limits, type restrictions, virus scanning
5. **Session Management**: Secure session storage with expiration

## Testing Strategy

### Unit Testing

```typescript
// Logic extraction tests
describe('FieldValidator', () => {
  it('should validate required fields', () => {
    const field = {
      id: 'test',
      kind: FieldKindEnum.SHORT_TEXT,
      validations: { required: true }
    };
    
    const result = FieldValidator.validate(field, '');
    expect(result.valid).toBe(false);
    expect(result.errors[0].code).toBe('REQUIRED');
  });
  
  it('should validate email format', () => {
    const field = {
      id: 'email',
      kind: FieldKindEnum.EMAIL
    };
    
    const result = FieldValidator.validate(field, 'invalid-email');
    expect(result.valid).toBe(false);
    expect(result.errors[0].code).toBe('INVALID_EMAIL');
  });
});
```

### Integration Testing

```typescript
// API endpoint tests
describe('Mobile API', () => {
  it('should create submission session', async () => {
    const response = await request(app)
      .post('/api/v1/submissions/start')
      .set('Authorization', 'Bearer ' + token)
      .send({ formId: 'test_form' });
      
    expect(response.status).toBe(201);
    expect(response.body.data).toHaveProperty('sessionId');
    expect(response.body.data).toHaveProperty('expiresAt');
  });
  
  it('should validate answers', async () => {
    const response = await request(app)
      .put('/api/v1/submissions/' + sessionId)
      .set('Authorization', 'Bearer ' + token)
      .send({
        answers: {
          email_field: 'invalid-email'
        }
      });
      
    expect(response.status).toBe(200);
    expect(response.body.data.validationResults.email_field.valid).toBe(false);
  });
});
```

### End-to-End Testing

```typescript
// Mobile client simulation
describe('Mobile Flow E2E', () => {
  it('should complete full form submission', async () => {
    // 1. Get form
    const form = await mobileApi.getForm('test_form');
    
    // 2. Start session
    const session = await mobileApi.startSubmission(form.id);
    
    // 3. Submit answers field by field
    for (const field of form.fields) {
      const answer = generateMockAnswer(field);
      await mobileApi.updateAnswer(session.id, field.id, answer);
    }
    
    // 4. Complete submission
    const result = await mobileApi.completeSubmission(session.id);
    expect(result.success).toBe(true);
  });
});
```

### Performance Testing

```yaml
# k6 load test script
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function() {
  let response = http.get('https://api.framna.com/api/v1/forms/test_form');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

## Implementation Checklist

### Pre-Implementation
- [ ] Create feature branch: `feature/api-first-migration`
- [ ] Set up development environment
- [ ] Back up production database
- [ ] Document current API usage

### Phase 1: Payment Removal
- [ ] Remove payment field type from enums
- [ ] Delete payment-related components
- [ ] Remove Stripe dependencies
- [ ] Update form validation to skip payments
- [ ] Migration script for existing forms
- [ ] Test form creation without payments

### Phase 2: UI Simplification
- [ ] Remove theme customization UI
- [ ] Simplify form preview
- [ ] Update form builder interface
- [ ] Remove style-related form settings
- [ ] Test simplified form creation

### Phase 3: API Development
- [ ] Create mobile API module
- [ ] Implement form retrieval endpoints
- [ ] Build submission management
- [ ] Add file upload endpoints
- [ ] Create API documentation
- [ ] Set up API versioning

### Phase 4: Logic Extraction
- [ ] Create form-logic package
- [ ] Extract validation logic
- [ ] Move conditional logic processing
- [ ] Refactor answer processing
- [ ] Remove UI dependencies
- [ ] Unit test all logic

### Phase 5: Testing
- [ ] Unit tests for all new code
- [ ] Integration tests for API
- [ ] E2E tests for mobile flow
- [ ] Performance testing
- [ ] Security audit
- [ ] User acceptance testing

### Phase 6: Documentation
- [ ] API reference documentation
- [ ] Mobile integration guide
- [ ] Migration guide for existing users
- [ ] Type definition packages
- [ ] Example mobile applications

### Phase 7: Deployment
- [ ] Deploy to staging environment
- [ ] Run migration scripts
- [ ] Smoke tests
- [ ] Gradual rollout
- [ ] Monitor error rates
- [ ] Full production deployment

### Post-Deployment
- [ ] Monitor API usage
- [ ] Gather mobile app feedback
- [ ] Performance optimization
- [ ] Bug fixes and patches
- [ ] Deprecate old endpoints

## Appendix

### A. File Structure Changes

```diff
packages/
+ form-logic/           # New pure logic package
+   src/
+     validation/
+     logic/
+     calculator/
+ mobile-api/           # New API types package
+   src/
+     dto/
+     interfaces/
  form-renderer/        # Refactored
-   src/blocks/Payment.tsx
-   src/theme.ts
    src/
      blocks/          # Simplified components
  server/              # Enhanced
+   src/module/mobile/
+   src/controller/api/
-   src/resolver/payment/
-   src/service/payment.service.ts
```

### B. Database Schema Changes

```javascript
// Remove payment fields
db.forms.updateMany({}, {
  $pull: {
    fields: { kind: "payment" }
  },
  $unset: {
    stripeAccount: "",
    "settings.stripePublishableKey": ""
  }
});

// Add mobile-specific fields
db.forms.updateMany({}, {
  $set: {
    "apiSettings": {
      "version": "1.0.0",
      "mobileEnabled": true,
      "deprecatedFields": []
    }
  }
});
```

### C. Environment Variables

```bash
# Remove
- STRIPE_PUBLISHABLE_KEY
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET

# Add
+ MOBILE_API_JWT_SECRET
+ MOBILE_API_RATE_LIMIT
+ S3_PRESIGNED_URL_EXPIRY
```

### D. Dependencies to Update

```json
// package.json changes
{
  "dependencies": {
    // Remove
    - "stripe": "^x.x.x",
    - "@radix-ui/react-*": "^x.x.x",
    - "tailwindcss": "^x.x.x",
    
    // Add
    + "@nestjs/swagger": "^6.0.0",
    + "joi": "^17.0.0",
    + "rate-limiter-flexible": "^2.0.0"
  }
}
```

---

This implementation guide serves as the authoritative reference for transforming Framna Feedback into an API-first platform. Follow each phase sequentially, ensuring thorough testing at each step. Regular updates to this document should be made as the implementation progresses and new insights are gained.