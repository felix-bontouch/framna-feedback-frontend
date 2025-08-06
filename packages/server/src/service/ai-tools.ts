// Tool definitions for OpenAI function calling

// Field kinds as string literals for JSON schema enum
const FIELD_KINDS = [
  'WELCOME',
  'THANK_YOU',
  'STATEMENT',
  'SHORT_TEXT',
  'LONG_TEXT',
  'NUMBER',
  'YES_NO',
  'MULTIPLE_CHOICE',
  'PICTURE_CHOICE',
  'FILE_UPLOAD',
  'OPINION_SCALE',
  'RATING',
  'DATE',
  'DATE_RANGE',
  'TIME',
  'INPUT_TABLE',
  'FULL_NAME',
  'ADDRESS',
  'EMAIL',
  'URL',
  'PHONE_NUMBER',
  'COUNTRY',
  'SIGNATURE',
  'LEGAL_TERMS'
] as const

const COMPARISON_OPERATORS = [
  'is',
  'is_not',
  'contains',
  'does_not_contain',
  'starts_with',
  'ends_with',
  'equal',
  'not_equal',
  'greater_than',
  'less_than',
  'greater_or_equal_than',
  'less_or_equal_than',
  'is_before',
  'is_after',
  'is_empty',
  'is_not_empty'
] as const

const ACTION_KINDS = ['navigate', 'calculate'] as const

const CALCULATE_OPERATORS = [
  'addition',
  'subtraction',
  'multiplication',
  'division',
  'assignment'
] as const

// Tool definitions
export const AI_TOOLS = {
  generateFormFields: {
    type: 'function' as const,
    function: {
      name: 'generate_form_fields',
      description: 'Generate professional form fields with logic analysis for a given topic',
      strict: true,
      parameters: {
        type: 'object',
        properties: {
          fields: {
            type: 'array',
            description: 'Array of form fields in logical order',
            items: {
              type: 'object',
              properties: {
                title: {
                  type: 'array',
                  description: 'Question text as array of strings',
                  items: { type: 'string' }
                },
                description: {
                  type: 'array',
                  description: 'Help text or instructions as array of strings',
                  items: { type: 'string' }
                },
                kind: {
                  type: 'string',
                  description: 'Type of form field',
                  enum: FIELD_KINDS
                },
                validations: {
                  type: 'object',
                  description: 'Validation rules for the field',
                  properties: {
                    required: { type: ['boolean', 'null'] },
                    min: { type: ['number', 'null'] },
                    max: { type: ['number', 'null'] },
                    minLength: { type: ['number', 'null'] },
                    maxLength: { type: ['number', 'null'] },
                    pattern: { type: ['string', 'null'] }
                  },
                  required: ['required', 'min', 'max', 'minLength', 'maxLength', 'pattern'],
                  additionalProperties: false
                },
                properties: {
                  type: 'object',
                  description: 'Field-specific properties',
                  properties: {
                    choices: {
                      type: 'array',
                      description: 'Options for choice fields',
                      items: {
                        type: 'object',
                        properties: {
                          label: { type: ['string', 'null'] }
                        },
                        required: ['label'],
                        additionalProperties: false
                      }
                    },
                    allowMultiple: { type: ['boolean', 'null'] },
                    allowOther: { type: ['boolean', 'null'] },
                    placeholder: { type: ['string', 'null'] },
                    format: { type: ['string', 'null'] },
                    min: { type: ['number', 'null'] },
                    max: { type: ['number', 'null'] },
                    step: { type: ['number', 'null'] },
                    rows: { type: ['number', 'null'] },
                    columns: { type: ['array', 'null'], items: { type: 'string' } }
                  },
                  required: [
                    'choices',
                    'allowMultiple',
                    'allowOther',
                    'placeholder',
                    'format',
                    'min',
                    'max',
                    'step',
                    'rows',
                    'columns'
                  ],
                  additionalProperties: false
                },
                statisticalPurpose: {
                  type: ['string', 'null'],
                  description: 'Statistical purpose of the field',
                  enum: ['demographic', 'screening', 'outcome', 'predictor', 'control', null]
                }
              },
              required: [
                'title',
                'description',
                'kind',
                'validations',
                'properties',
                'statisticalPurpose'
              ],
              additionalProperties: false
            }
          },
          logicAnalysis: {
            type: 'object',
            description: 'Analysis of whether and how logic should be applied',
            properties: {
              isLogicNeeded: {
                type: ['boolean', 'null'],
                description: 'Whether conditional logic would enhance the form'
              },
              complexity: {
                type: ['string', 'null'],
                description: 'Complexity level of required logic',
                enum: ['simple', 'moderate', 'complex', null]
              },
              reasoning: {
                type: ['string', 'null'],
                description: 'Explanation of why logic is or is not needed'
              },
              logicSuggestions: {
                type: ['array', 'null'],
                description: 'Specific logic suggestions for the form',
                items: { type: 'string' }
              }
            },
            required: ['isLogicNeeded', 'complexity', 'reasoning', 'logicSuggestions'],
            additionalProperties: false
          }
        },
        required: ['fields', 'logicAnalysis'],
        additionalProperties: false
      }
    }
  },

  generateAdditionalFields: {
    type: 'function' as const,
    function: {
      name: 'generate_additional_fields',
      description: 'Generate additional form fields that complement existing fields',
      strict: true,
      parameters: {
        type: 'object',
        properties: {
          fields: {
            type: 'array',
            description: 'Array of additional form fields',
            items: {
              type: 'object',
              properties: {
                title: {
                  type: 'array',
                  description: 'Question text as array of strings',
                  items: { type: 'string' }
                },
                description: {
                  type: 'array',
                  description: 'Help text or instructions as array of strings',
                  items: { type: 'string' }
                },
                kind: {
                  type: 'string',
                  description: 'Type of form field',
                  enum: FIELD_KINDS
                },
                validations: {
                  type: 'object',
                  properties: {
                    required: { type: ['boolean', 'null'] },
                    min: { type: ['number', 'null'] },
                    max: { type: ['number', 'null'] },
                    minLength: { type: ['number', 'null'] },
                    maxLength: { type: ['number', 'null'] },
                    pattern: { type: ['string', 'null'] }
                  },
                  required: ['required', 'min', 'max', 'minLength', 'maxLength', 'pattern'],
                  additionalProperties: false
                },
                properties: {
                  type: 'object',
                  properties: {
                    choices: {
                      type: 'array',
                      items: {
                        type: 'object',
                        properties: {
                          label: { type: ['string', 'null'] }
                        },
                        required: ['label'],
                        additionalProperties: false
                      }
                    },
                    allowMultiple: { type: ['boolean', 'null'] },
                    allowOther: { type: ['boolean', 'null'] },
                    placeholder: { type: ['string', 'null'] }
                  },
                  required: ['choices', 'allowMultiple', 'allowOther', 'placeholder'],
                  additionalProperties: false
                }
              },
              required: ['title', 'description', 'kind', 'validations', 'properties'],
              additionalProperties: false
            }
          }
        },
        required: ['fields'],
        additionalProperties: false
      }
    }
  },

  generateFormLogic: {
    type: 'function' as const,
    function: {
      name: 'generate_form_logic',
      description: 'Generate conditional logic rules for form fields',
      strict: true,
      parameters: {
        type: 'object',
        properties: {
          logics: {
            type: 'array',
            description: 'Array of logic rules',
            items: {
              type: 'object',
              properties: {
                fieldId: {
                  type: 'string',
                  description: 'ID of the source field that triggers the logic'
                },
                fieldTitle: {
                  type: 'string',
                  description: 'Title of the source field (used if fieldId not available)'
                },
                payloads: {
                  type: 'array',
                  description: 'Array of conditions and actions',
                  items: {
                    type: 'object',
                    properties: {
                      condition: {
                        type: 'object',
                        description: 'Condition that triggers the action',
                        properties: {
                          comparison: {
                            type: 'string',
                            description: 'Comparison operator',
                            enum: COMPARISON_OPERATORS
                          },
                          expected: {
                            type: ['string', 'number', 'array', 'null'],
                            description: 'Expected value for comparison',
                            items: { type: 'string' }
                          },
                          ref: {
                            type: 'string',
                            description: 'Reference to variable for dynamic comparison'
                          }
                        },
                        required: ['comparison', 'expected', 'ref'],
                        additionalProperties: false
                      },
                      action: {
                        type: 'object',
                        description: 'Action to take when condition is met',
                        properties: {
                          kind: {
                            type: 'string',
                            description: 'Type of action',
                            enum: ACTION_KINDS
                          },
                          fieldId: {
                            type: 'string',
                            description: 'Target field ID for navigate action'
                          },
                          fieldTitle: {
                            type: 'string',
                            description: 'Target field title (used if fieldId not available)'
                          },
                          variable: {
                            type: 'string',
                            description: 'Variable name for calculate action'
                          },
                          operator: {
                            type: 'string',
                            description: 'Calculation operator',
                            enum: CALCULATE_OPERATORS
                          },
                          value: {
                            type: ['string', 'number', 'null'],
                            description: 'Value for calculation'
                          },
                          ref: {
                            type: 'string',
                            description: 'Reference to field or variable for calculation'
                          }
                        },
                        required: [
                          'kind',
                          'fieldId',
                          'fieldTitle',
                          'variable',
                          'operator',
                          'value',
                          'ref'
                        ],
                        additionalProperties: false
                      }
                    },
                    required: ['condition', 'action'],
                    additionalProperties: false
                  }
                }
              },
              required: ['payloads', 'fieldId', 'fieldTitle'],
              additionalProperties: false
            }
          }
        },
        required: ['logics'],
        additionalProperties: false
      }
    }
  }
}

// Helper function to get the appropriate tool for each method
export function getToolForMethod(methodName: string) {
  const toolMap: Record<string, any> = {
    generateFormFields: AI_TOOLS.generateFormFields,
    generateAdditionalFields: AI_TOOLS.generateAdditionalFields,
    generateFormLogic: AI_TOOLS.generateFormLogic,
    generateInitialFormLogic: AI_TOOLS.generateFormLogic
  }

  return toolMap[methodName]
}
