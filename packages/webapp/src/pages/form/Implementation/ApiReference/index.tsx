import { IconApi } from '@tabler/icons-react'
import { useMemo } from 'react'

import { fieldTypes, generateSubmissionExample, transformFormForMobile } from './utils'

import { useFormStore } from '@/store'

import CodeExample from './CodeExample'
import EndpointSection from './EndpointSection'
import ParameterTable from './ParameterTable'
import ResponseSchema from './ResponseSchema'

interface ApiReferenceProps {
  formId: string
  shareLink: string
}

export default function ApiReference({ formId }: ApiReferenceProps) {
  const { form } = useFormStore()
  const baseApiUrl = import.meta.env.VITE_API_URL || 'https://api.framna.com'

  // Transform form data for examples
  const exampleFormResponse = useMemo(() => {
    const transformed = transformFormForMobile(form, formId)

    if (!transformed) {
      // Fallback example
      return {
        id: formId,
        name: 'Customer Feedback Form',
        description: 'Help us improve our service',
        settings: {
          active: true,
          requirePassword: false,
          captchaKind: 'none',
          locale: 'en'
        },
        fields: [
          {
            id: 'field_1',
            kind: 'short_text',
            title: 'What is your name?',
            validations: { required: true },
            properties: { placeholder: 'Enter your name' }
          }
        ],
        logics: [],
        variables: []
      }
    }

    return transformed
  }, [form, formId])

  const exampleSubmissionRequest = useMemo(() => {
    return generateSubmissionExample(exampleFormResponse)
  }, [exampleFormResponse])

  // GET Form endpoint parameters
  const getFormParameters = [
    {
      name: 'formId',
      type: 'string',
      required: true,
      description: 'The unique identifier of the form',
      example: formId
    }
  ]

  // POST Submit parameters
  const submitBodyParameters = [
    {
      name: 'answers',
      type: 'object',
      required: true,
      description: 'Key-value pairs where keys are field IDs and values are the user responses'
    },
    {
      name: 'startedAt',
      type: 'number',
      required: true,
      description: 'Unix timestamp (milliseconds) when the user started filling the form'
    },
    {
      name: 'clientInfo',
      type: 'object',
      required: true,
      description: 'Information about the client submitting the form',
      children: [
        { name: 'ip', type: 'string', required: true, description: 'IP address of the client' },
        {
          name: 'userAgent',
          type: 'string',
          required: true,
          description: 'User agent string of the client'
        },
        {
          name: 'os',
          type: 'string',
          required: true,
          description: 'Operating system (iOS, Android, etc.)'
        },
        {
          name: 'osVersion',
          type: 'string',
          required: true,
          description: 'OS version (e.g., 16.0, 13)'
        },
        { name: 'appVersion', type: 'string', required: true, description: 'Mobile app version' },
        { name: 'device', type: 'string', required: true, description: 'Device model/name' },
        {
          name: 'deviceId',
          type: 'string',
          required: false,
          description: 'Unique device identifier'
        },
        {
          name: 'locale',
          type: 'string',
          required: false,
          description: 'Device locale/language (e.g., en-US)'
        }
      ]
    },
    {
      name: 'hiddenFields',
      type: 'array',
      required: false,
      description: 'Hidden field values to be submitted with the form'
    },
    {
      name: 'password',
      type: 'string',
      required: false,
      description: 'Password if the form requires password protection'
    },
    {
      name: 'captchaToken',
      type: 'string',
      required: false,
      description: 'Captcha verification token if the form has captcha enabled'
    },
    {
      name: 'category',
      type: 'string',
      required: false,
      description: 'Feedback category for mobile forms',
      enum: ['NPS', 'FEATURE', 'USER_FLOW', 'PERFORMANCE', 'GENERAL', 'ONBOARDING', 'RATING']
    }
  ]

  // Response schema for GET form
  const formResponseSchema = [
    { name: 'id', type: 'string', description: 'Unique identifier of the form', required: true },
    { name: 'name', type: 'string', description: 'Display name of the form', required: true },
    { name: 'description', type: 'string', description: 'Form description', required: false },
    {
      name: 'settings',
      type: 'object',
      description: 'Form configuration settings',
      required: true,
      children: [
        {
          name: 'active',
          type: 'boolean',
          description: 'Whether the form is currently accepting responses'
        },
        {
          name: 'requirePassword',
          type: 'boolean',
          description: 'Whether password is required to access the form'
        },
        {
          name: 'captchaKind',
          type: 'string',
          description: 'Type of captcha protection (none, recaptcha, etc.)'
        },
        { name: 'locale', type: 'string', description: 'Default language locale for the form' },
        { name: 'redirectUrl', type: 'string', description: 'URL to redirect after submission' }
      ]
    },
    {
      name: 'fields',
      type: 'array',
      description: 'Array of form fields',
      required: true,
      children: [
        { name: 'id', type: 'string', description: 'Unique identifier of the field' },
        { name: 'kind', type: 'string', description: 'Field type (see field types reference)' },
        { name: 'title', type: 'string', description: 'Field label/question text' },
        { name: 'description', type: 'string', description: 'Additional help text for the field' },
        { name: 'validations', type: 'object', description: 'Validation rules for the field' },
        { name: 'properties', type: 'object', description: 'Field-specific configuration' }
      ]
    },
    { name: 'logics', type: 'array', description: 'Conditional logic rules', required: true },
    { name: 'variables', type: 'array', description: 'Dynamic variables', required: true }
  ]

  // Response schema for submit
  const submitResponseSchema = [
    {
      name: 'success',
      type: 'boolean',
      description: 'Whether the submission was successful',
      required: true
    },
    {
      name: 'submissionId',
      type: 'string',
      description: 'Unique identifier for this submission',
      required: true
    },
    {
      name: 'timestamp',
      type: 'number',
      description: 'Unix timestamp of the submission',
      required: true
    },
    {
      name: 'redirectUrl',
      type: 'string',
      description: 'URL to redirect if configured',
      required: false
    },
    { name: 'message', type: 'string', description: 'Success or error message', required: true }
  ]

  const curlGetForm = `curl -X GET \\
  ${baseApiUrl}/api/mobile/forms/${formId} \\
  -H "Accept: application/json"`

  const curlSubmitForm = `curl -X POST \\
  ${baseApiUrl}/api/mobile/forms/${formId} \\
  -H "Content-Type: application/json" \\
  -d '${JSON.stringify(exampleSubmissionRequest, null, 2)}'`

  return (
    <section className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="flex items-center gap-2 text-xl font-semibold">
          <IconApi className="h-5 w-5" />
          API Reference
        </h2>
        <p className="text-secondary mt-2 text-sm">
          REST API endpoints for fetching form structure and submitting responses in mobile
          applications
        </p>
      </div>

      {/* API Endpoints */}
      <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
        {/* GET Form Endpoint */}
        <EndpointSection
          method="GET"
          path={`/api/mobile/forms/:formId`}
          description="Retrieve the complete form structure including all fields, settings, and configuration needed to render the form in a mobile application."
          examples={
            <>
              <CodeExample title="cURL" code={curlGetForm} language="bash" />
              <CodeExample
                title="Response"
                code={JSON.stringify(exampleFormResponse, null, 2)}
                language="json"
              />
            </>
          }
        >
          <ParameterTable title="Path Parameters" parameters={getFormParameters} />

          <ResponseSchema title="Response Schema" fields={formResponseSchema} />

          <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-800 dark:bg-blue-900/20">
            <h4 className="mb-2 text-sm font-medium text-blue-900 dark:text-blue-100">Notes</h4>
            <ul className="list-inside list-disc space-y-1 text-xs text-blue-800 dark:text-blue-200">
              <li>Only active and non-suspended forms will return data</li>
              <li>Visual styling properties are stripped from the response</li>
              <li>Use the field kind to determine the appropriate native UI component</li>
            </ul>
          </div>
        </EndpointSection>

        {/* POST Submit Endpoint */}
        <EndpointSection
          method="POST"
          path={`/api/mobile/forms/:formId`}
          description="Submit form responses. The request body should contain answers mapped to field IDs along with metadata about the submission."
          examples={
            <>
              <CodeExample title="cURL" code={curlSubmitForm} language="bash" />
              <CodeExample
                title="Request Body"
                code={JSON.stringify(exampleSubmissionRequest, null, 2)}
                language="json"
              />
              <CodeExample
                title="Success Response"
                code={JSON.stringify(
                  {
                    success: true,
                    submissionId: 'sub_abc123xyz',
                    timestamp: Date.now(),
                    redirectUrl: exampleFormResponse?.settings?.redirectUrl || null,
                    message: 'Form submitted successfully'
                  },
                  null,
                  2
                )}
                language="json"
              />
            </>
          }
        >
          <ParameterTable title="Path Parameters" parameters={getFormParameters} />

          <ParameterTable title="Request Body" parameters={submitBodyParameters} />

          <ResponseSchema title="Response Schema" fields={submitResponseSchema} />

          <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 dark:border-amber-800 dark:bg-amber-900/20">
            <h4 className="mb-2 text-sm font-medium text-amber-900 dark:text-amber-100">
              Validation
            </h4>
            <ul className="list-inside list-disc space-y-1 text-xs text-amber-800 dark:text-amber-200">
              <li>All required fields must have corresponding answers</li>
              <li>Field validations (min/max, regex, etc.) are enforced server-side</li>
              <li>
                The <code className="rounded bg-amber-100 px-1 dark:bg-amber-800">startedAt</code>{' '}
                timestamp is used for time-based analytics
              </li>
              <li>
                Include accurate{' '}
                <code className="rounded bg-amber-100 px-1 dark:bg-amber-800">clientInfo</code> for
                detailed analytics
              </li>
            </ul>
          </div>
        </EndpointSection>
      </div>

      {/* Field Types Reference */}
      <div className="rounded-lg border border-slate-200 p-6 dark:border-slate-700">
        <h3 className="mb-4 text-lg font-semibold">Field Types Reference</h3>
        <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
          Each field in the form response includes a{' '}
          <code className="rounded bg-slate-100 px-1 dark:bg-slate-800">kind</code> property that
          indicates the type of input expected.
        </p>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {fieldTypes.map(({ kind, description, example }) => (
            <div key={kind} className="flex flex-col space-y-1">
              <div className="flex items-baseline gap-2">
                <code className="rounded bg-slate-100 px-2 py-1 font-mono text-xs dark:bg-slate-800">
                  {kind}
                </code>
                <span className="text-xs text-slate-600 dark:text-slate-400">{description}</span>
              </div>
              <span className="ml-2 text-xs text-slate-500 dark:text-slate-500">
                Returns: <code className="text-slate-700 dark:text-slate-300">{example}</code>
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Implementation Guide */}
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-6 dark:border-slate-700 dark:bg-slate-900">
        <h3 className="mb-4 text-lg font-semibold">Implementation Guide</h3>
        <div className="space-y-4 text-sm text-slate-600 dark:text-slate-400">
          <div>
            <h4 className="mb-2 font-medium text-slate-900 dark:text-slate-100">
              1. Fetch Form Structure
            </h4>
            <p>
              Call the GET endpoint to retrieve the form configuration. Cache this response to avoid
              unnecessary API calls.
            </p>
          </div>
          <div>
            <h4 className="mb-2 font-medium text-slate-900 dark:text-slate-100">
              2. Render Native UI
            </h4>
            <p>
              Use the <code className="rounded bg-slate-100 px-1 dark:bg-slate-800">kind</code>{' '}
              property of each field to determine which native UI component to render. The{' '}
              <code className="rounded bg-slate-100 px-1 dark:bg-slate-800">properties</code> object
              contains field-specific configuration.
            </p>
          </div>
          <div>
            <h4 className="mb-2 font-medium text-slate-900 dark:text-slate-100">
              3. Collect Responses
            </h4>
            <p>
              As users interact with the form, collect their responses in an object where keys are
              field IDs and values are the user inputs.
            </p>
          </div>
          <div>
            <h4 className="mb-2 font-medium text-slate-900 dark:text-slate-100">4. Submit Form</h4>
            <p>
              Send the collected responses along with metadata to the POST endpoint. Handle success
              and error responses appropriately.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
