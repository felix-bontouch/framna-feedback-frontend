export const transformFormForMobile = (form: any, formId: string) => {
  if (!form) return null

  // Transform settings - keep only functional settings
  const transformSettings = (settings: any) => {
    if (!settings) return {}

    const functionalSettings = [
      'captchaKind',
      'active',
      'enableExpirationDate',
      'expirationTimeZone',
      'enabledAt',
      'closedAt',
      'enableTimeLimit',
      'timeLimit',
      'filterSpam',
      'allowArchive',
      'requirePassword',
      'redirectOnCompletion',
      'redirectUrl',
      'redirectDelay',
      'enableQuotaLimit',
      'quotaLimit',
      'enableIpLimit',
      'ipLimitCount',
      'ipLimitTime',
      'enableProgress',
      'enableQuestionList',
      'enableNavigationArrows',
      'locale',
      'languages',
      'enableClosedMessage',
      'closedFormTitle',
      'closedFormDescription',
      'enableEmailNotification'
    ]

    return functionalSettings.reduce((acc, key) => {
      if (settings[key] !== undefined) {
        acc[key] = settings[key]
      }
      return acc
    }, {} as any)
  }

  // Transform properties - keep only functional properties
  const transformProperties = (properties: any) => {
    if (!properties) return {}

    const functionalProperties = [
      // Choice properties
      'choices',
      'allowOther',
      'allowMultiple',
      'other',
      'randomize',
      // Text properties
      'placeholder',
      // Number/rating properties
      'total',
      'start',
      'leftLabel',
      'centerLabel',
      'rightLabel',
      'hideMarks',
      // Date/time properties
      'format',
      'allowTime',
      'use12Hours',
      // Phone properties
      'defaultCountryCode',
      // Table properties
      'tableColumns',
      // Other properties
      'score',
      'sourceUrl',
      'badge',
      'fields',
      'showButton',
      'buttonText',
      'buttonLinkUrl'
    ]

    const result: any = {}

    functionalProperties.forEach(key => {
      if (properties[key] !== undefined) {
        result[key] = properties[key]
      }
    })

    // Special handling for choices to remove visual properties
    if (result.choices) {
      result.choices = result.choices.map((choice: any) => ({
        id: choice.id,
        label: choice.label,
        score: choice.score,
        isExpected: choice.isExpected
      }))
    }

    return result
  }

  // Transform fields
  const transformFields = (fields: any[]) => {
    if (!fields || !Array.isArray(fields)) return []

    return fields.map(field => {
      const mobileField: any = {
        id: field.id,
        kind: field.kind,
        title: field.title,
        description: field.description,
        validations: field.validations || {},
        width: field.width,
        hide: field.hide,
        frozen: field.frozen
      }

      if (field.properties) {
        mobileField.properties = transformProperties(field.properties)

        // Recursively transform nested fields (for GROUP fields)
        if (field.properties.fields) {
          mobileField.properties.fields = transformFields(field.properties.fields)
        }
      }

      return mobileField
    })
  }

  return {
    id: form.id || formId,
    teamId: form.teamId,
    projectId: form.projectId,
    memberId: form.memberId,
    name: form.name,
    description: form.description,
    interactiveMode: form.interactiveMode,
    kind: form.kind,
    settings: transformSettings(form.settings),
    fields: transformFields(form.drafts || form.fields || []),
    hiddenFields: form.hiddenFields || [],
    logics: form.logics || [],
    variables: form.variables || [],
    translations: form.translations || {},
    fieldsUpdatedAt: form.fieldsUpdatedAt || Date.now(),
    retentionAt: form.retentionAt,
    suspended: form.suspended || false,
    isDraft: false,
    status: form.status,
    version: form.version || 1
  }
}

export const generateSubmissionExample = (form: any) => {
  if (!form?.fields || form.fields.length === 0) {
    // Fallback example
    return {
      answers: {
        field_1: 'John Doe'
      },
      startedAt: Date.now(),
      clientInfo: {
        ip: '192.168.1.1',
        userAgent: 'MobileApp/1.0 (iOS 16.0)',
        os: 'iOS',
        osVersion: '16.0',
        appVersion: '1.0.0',
        device: 'iPhone 14 Pro',
        deviceId: '550e8400-e29b-41d4-a716-446655440000',
        locale: 'en-US'
      },
      category: 'GENERAL'
    }
  }

  // Generate sample answers based on field types
  const answers: Record<string, any> = {}

  form.fields.forEach((field: any) => {
    // Skip hidden fields
    if (field.hide) return

    switch (field.kind) {
      case 'short_text':
        answers[field.id] = 'Sample text answer'
        break
      case 'long_text':
        answers[field.id] = 'This is a longer sample answer that might span multiple lines.'
        break
      case 'multiple_choice':
        const choices = field.properties?.choices
        if (choices && choices.length > 0) {
          answers[field.id] = field.properties.allowMultiple
            ? [choices[0].id, choices[1]?.id].filter(Boolean)
            : choices[0].id
        }
        break
      case 'dropdown':
        const dropdownChoices = field.properties?.choices
        if (dropdownChoices && dropdownChoices.length > 0) {
          answers[field.id] = dropdownChoices[0].id
        }
        break
      case 'email':
        answers[field.id] = 'user@example.com'
        break
      case 'phone_number':
        answers[field.id] = '+1234567890'
        break
      case 'number':
        answers[field.id] = 42
        break
      case 'date':
        answers[field.id] = new Date().toISOString().split('T')[0]
        break
      case 'time':
        answers[field.id] = '14:30'
        break
      case 'rating':
        answers[field.id] = 4
        break
      case 'scale':
        answers[field.id] = 7
        break
      case 'yes_no':
        answers[field.id] = true
        break
      case 'legal':
        answers[field.id] = true
        break
      case 'file_upload':
        answers[field.id] = {
          filename: 'document.pdf',
          size: 1024000,
          url: 'https://storage.example.com/uploads/document.pdf'
        }
        break
    }
  })

  return {
    answers,
    startedAt: Date.now(),
    clientInfo: {
      ip: '192.168.1.1',
      userAgent: 'MobileApp/1.0 (iOS 16.0)',
      os: 'iOS',
      osVersion: '16.0',
      appVersion: '1.0.0',
      device: 'iPhone 14 Pro',
      deviceId: '550e8400-e29b-41d4-a716-446655440000',
      locale: 'en-US'
    },
    category: 'GENERAL',
    hiddenFields:
      form.hiddenFields?.length > 0
        ? [
            {
              id: form.hiddenFields[0].id || 'source',
              value: 'mobile_app'
            }
          ]
        : undefined
  }
}

export const fieldTypes = [
  { kind: 'short_text', description: 'Single line text input', example: 'string' },
  { kind: 'long_text', description: 'Multi-line text area', example: 'string' },
  {
    kind: 'multiple_choice',
    description: 'Radio buttons or checkboxes',
    example: 'string | string[]'
  },
  { kind: 'dropdown', description: 'Dropdown selection', example: 'string' },
  { kind: 'email', description: 'Email input with validation', example: 'string' },
  { kind: 'phone_number', description: 'Phone number with country code', example: 'string' },
  { kind: 'number', description: 'Numeric input', example: 'number' },
  { kind: 'date', description: 'Date picker', example: 'string (YYYY-MM-DD)' },
  { kind: 'time', description: 'Time picker', example: 'string (HH:mm)' },
  { kind: 'file_upload', description: 'File upload', example: 'object' },
  { kind: 'rating', description: 'Star or numeric rating', example: 'number' },
  { kind: 'scale', description: 'Linear scale (e.g., 1-10)', example: 'number' },
  { kind: 'yes_no', description: 'Binary yes/no choice', example: 'boolean' },
  { kind: 'legal', description: 'Terms acceptance checkbox', example: 'boolean' }
]

export const httpMethods = {
  GET: {
    color: 'text-green-600 bg-green-50 border-green-200',
    darkColor: 'dark:text-green-400 dark:bg-green-900/20 dark:border-green-800'
  },
  POST: {
    color: 'text-blue-600 bg-blue-50 border-blue-200',
    darkColor: 'dark:text-blue-400 dark:bg-blue-900/20 dark:border-blue-800'
  },
  PUT: {
    color: 'text-orange-600 bg-orange-50 border-orange-200',
    darkColor: 'dark:text-orange-400 dark:bg-orange-900/20 dark:border-orange-800'
  },
  DELETE: {
    color: 'text-red-600 bg-red-50 border-red-200',
    darkColor: 'dark:text-red-400 dark:bg-red-900/20 dark:border-red-800'
  }
}
