# Current API Usage Documentation

Generated on: 2025-08-04
Purpose: Document existing API endpoints before migration to API-first architecture

## GraphQL API Endpoints

### Authentication & User Management

#### Mutations
- `login(email: String!, password: String!): LoginResponse`
- `signup(email: String!, password: String!): SignupResponse`
- `resetPassword(token: String!, password: String!): Result`
- `sendResetPasswordEmail(email: String!): Result`
- `updateUserPassword(oldPassword: String!, newPassword: String!): Result`
- `verifyEmail(code: String!): Result`

### Form Management

#### Queries
- `form(id: ID!): Form`
- `forms(projectId: ID!): [Form]`
- `searchForms(keyword: String!): [Form]`

#### Mutations
- `createForm(input: CreateFormInput!): Form`
- `updateForm(id: ID!, input: UpdateFormInput!): Form`
- `deleteForm(id: ID!): Result`
- `duplicateForm(id: ID!): Form`
- `publishForm(id: ID!): Form`
- `moveFormToTrash(id: ID!): Result`
- `restoreForm(id: ID!): Result`

### Form Structure Updates

#### Mutations
- `updateFormSchemas(id: ID!, fields: [FieldInput]!): Form`
- `updateFormLogics(id: ID!, logics: [LogicInput]!): Form`
- `updateFormVariables(id: ID!, variables: [VariableInput]!): Form`
- `updateFormHiddenFields(id: ID!, hiddenFields: [HiddenFieldInput]!): Form`
- `updateFormTheme(id: ID!, theme: ThemeInput!): Form`

### Submission Management

#### Queries
- `submission(id: ID!): Submission`
- `submissions(formId: ID!, pagination: PaginationInput): SubmissionConnection`
- `submissionAnswers(id: ID!): [Answer]`

#### Mutations
- `deleteSubmission(id: ID!): Result`
- `updateSubmissionAnswer(id: ID!, fieldId: ID!, value: JSON!): Result`
- `updateSubmissionsCategory(ids: [ID]!, category: SubmissionCategory!): Result`

### Public Form Endpoints (No Auth Required)

#### Queries
- `openForm(input: OpenFormInput!): String` - Returns encrypted token
- `formPassword(input: VerifyPasswordInput!): String` - Verify form password

#### Mutations
- `completeSubmission(input: CompleteSubmissionInput!): CompleteSubmissionType`

### Payment Integration (TO BE REMOVED)

#### Queries
- `stripeAuthorizeUrl(): String`
- `connectStripe(code: String!): Result`

#### Mutations
- `revokeStripeAccount(): Result`

### Integration Management

#### Mutations
- `updateIntegrationSettings(formId: ID!, kind: IntegrationKind!, settings: JSON!): Result`
- `updateIntegrationStatus(formId: ID!, kind: IntegrationKind!, status: Boolean!): Result`
- `deleteIntegrationSettings(formId: ID!, kind: IntegrationKind!): Result`

## REST API Endpoints

### Form Rendering
- `GET /form/:formId` - Returns HTML page for form rendering

### File Upload
- `POST /upload` - File upload endpoint (requires auth)
- `GET /image/:key` - Retrieve uploaded images

### Health Check
- `GET /health` - Application health status

### Export
- `GET /export-submissions/:formId` - Export submissions as CSV/Excel

### Webhooks
- `POST /payment-intent-webhook` - Stripe webhook (TO BE REMOVED)

## Authentication Methods

### GraphQL
- JWT tokens in Authorization header: `Bearer <token>`
- Cookies for web sessions

### REST
- Same JWT tokens as GraphQL
- Session cookies for form submissions

## Current Data Flow

### Form Creation
1. User creates form via webapp (GraphQL)
2. Form definition stored in MongoDB
3. Form can be published/unpublished

### Form Submission
1. End user opens form (`openForm` query)
2. Receives encrypted token
3. Submits answers (`completeSubmission` mutation)
4. Answers validated server-side
5. Submission stored in MongoDB
6. Webhooks/integrations triggered

### File Handling
1. Request upload permission
2. Upload file to server
3. Server stores in local filesystem or S3
4. Return file reference

## Rate Limiting

- GraphQL endpoints: 100 requests per minute per IP
- Public submission: 10 submissions per minute per IP
- File uploads: 10 per minute per user

## Field Types Supported

All 30+ field types listed in `FieldKindEnum`:
- Input: SHORT_TEXT, LONG_TEXT, NUMBER
- Choice: YES_NO, MULTIPLE_CHOICE, PICTURE_CHOICE
- Date/Time: DATE, DATE_RANGE, TIME
- Contact: EMAIL, PHONE_NUMBER, ADDRESS, FULL_NAME
- Files: FILE_UPLOAD, SIGNATURE
- Payment: PAYMENT (TO BE REMOVED)
- Others: RATING, OPINION_SCALE, COUNTRY, URL, LEGAL_TERMS

## Integration Points

### Current Integrations
- Google Analytics
- Facebook Pixel
- Webhooks
- Email notifications

### Authentication Providers
- Email/Password
- Google OAuth
- Apple Sign In

## Notes for Migration

1. **Preserve**: All form CRUD operations, submission handling, file uploads
2. **Remove**: Payment endpoints, Stripe integration
3. **Add**: Mobile-specific endpoints, session management, better file handling
4. **Modify**: Response formats for mobile optimization