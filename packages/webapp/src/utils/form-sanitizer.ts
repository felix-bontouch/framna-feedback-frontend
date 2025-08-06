import { nanoid } from '@heyform-inc/utils'

/**
 * Sanitizes form field data to match GraphQL schema requirements
 * Removes null/undefined fields that aren't accepted by the backend
 */
export function sanitizeFormField(field: any): any {
  const sanitized: any = {
    id: field.id,
    kind: field.kind,
    title: field.title,
    description: field.description
  }

  // Sanitize validations - only include fields that are defined in ValidationInput
  if (field.validations) {
    const validations: any = {}

    // Only include these fields if they're not null/undefined
    if (field.validations.required !== null && field.validations.required !== undefined) {
      validations.required = field.validations.required
    }
    if (field.validations.min !== null && field.validations.min !== undefined) {
      validations.min = field.validations.min
    }
    if (field.validations.max !== null && field.validations.max !== undefined) {
      validations.max = field.validations.max
    }
    if (field.validations.matchExpected !== null && field.validations.matchExpected !== undefined) {
      validations.matchExpected = field.validations.matchExpected
    }

    // Only add validations if it has at least one property
    if (Object.keys(validations).length > 0) {
      sanitized.validations = validations
    }
  }

  // Sanitize properties - only include fields that are defined in PropertyInput
  if (field.properties) {
    const properties: any = {}

    // Handle choices array - ensure each choice has an id
    if (field.properties.choices && Array.isArray(field.properties.choices)) {
      properties.choices = field.properties.choices.map((choice: any) => {
        if (typeof choice === 'string') {
          return { id: nanoid(8), label: choice }
        }
        // Ensure choice has an id
        if (!choice.id) {
          return { id: nanoid(8), label: choice.label || '', image: choice.image }
        }
        return choice
      })
    }

    // Only include these fields if they're not null/undefined
    const allowedProperties = [
      'showButton',
      'buttonText',
      'hideMarks',
      'allowOther',
      'allowMultiple',
      'badge',
      'verticalAlignment',
      'randomize',
      'choiceStyle',
      'other',
      'numberPreRow',
      'shape',
      'hidden',
      'referral',
      'redirectOnCompletion',
      'redirectUrl',
      'fields',
      'hideQuota',
      'allowTextEntry',
      'allowDuplication',
      'recaptchaSiteKey',
      'geetestCaptchaId',
      'currency',
      'locale',
      'subscriptionPlans',
      'products',
      'stripe',
      'stripeAccount',
      'addressType',
      'color',
      'defaultValue',
      'leftLabel',
      'centerLabel',
      'rightLabel',
      'multipleSelection',
      'style',
      'display',
      'total',
      'subscriptionPlanTotal',
      'tableColumns'
    ]

    allowedProperties.forEach(prop => {
      if (field.properties[prop] !== null && field.properties[prop] !== undefined) {
        properties[prop] = field.properties[prop]
      }
    })

    // Only add properties if it has at least one property
    if (Object.keys(properties).length > 0) {
      sanitized.properties = properties
    }
  }

  // Add layout if present and not null
  if (field.layout) {
    sanitized.layout = field.layout
  }

  // Add width if present
  if (field.width !== undefined) {
    sanitized.width = field.width
  }

  // Add hide if present
  if (field.hide !== undefined) {
    sanitized.hide = field.hide
  }

  // Add frozen if present
  if (field.frozen !== undefined) {
    sanitized.frozen = field.frozen
  }

  return sanitized
}

/**
 * Sanitizes all form fields before publishing
 */
export function sanitizeFormDrafts(drafts: any[]): any[] {
  if (!Array.isArray(drafts)) {
    return []
  }

  return drafts.map(sanitizeFormField)
}
