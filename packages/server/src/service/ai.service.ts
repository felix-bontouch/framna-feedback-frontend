import { FieldKindEnum } from '@heyform-inc/shared-types-enums'
import { Injectable } from '@nestjs/common'
import OpenAI from 'openai'

import { OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_GPT_MODEL } from '@environments'
import { nanoid } from '@heyform-inc/utils'

interface GeneratedField {
  id: string
  title: any[]
  description?: any[]
  kind: FieldKindEnum
  validations?: {
    required?: boolean
    min?: number
    max?: number
  }
  properties?: any
}

@Injectable()
export class AIService {
  private openai: OpenAI | null = null

  constructor() {
    if (OPENAI_API_KEY) {
      this.openai = new OpenAI({
        apiKey: OPENAI_API_KEY,
        baseURL: OPENAI_BASE_URL
      })
    }
  }

  async generateFormFields(topic: string, reference?: string): Promise<GeneratedField[]> {
    if (!this.openai) {
      throw new Error('OpenAI API is not configured')
    }

    const prompt = this.buildFormGenerationPrompt(topic, reference)

    try {
      const response = await this.openai.chat.completions.create({
        model: OPENAI_GPT_MODEL,
        messages: [
          {
            role: 'system',
            content:
              'You are a form builder assistant. Generate form fields based on the given topic and requirements. Return a JSON array of form fields.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        response_format: { type: 'json_object' }
      })

      const content = response.choices[0]?.message?.content
      if (!content) {
        throw new Error('No response from OpenAI')
      }

      const result = JSON.parse(content)
      const fields = result.fields || []

      return this.mapToFormFields(fields)
    } catch (error) {
      console.error('Error generating form fields:', error)
      throw new Error('Failed to generate form fields')
    }
  }

  async generateAdditionalFields(existingFields: any[], prompt: string): Promise<GeneratedField[]> {
    if (!this.openai) {
      throw new Error('OpenAI API is not configured')
    }

    const systemPrompt = `You are a form builder assistant. Based on the existing form fields and the user's request, generate additional form fields that complement the existing ones. Return a JSON array of new form fields.
    
Existing fields context: ${JSON.stringify(existingFields.map(f => ({ title: f.title, kind: f.kind })))}`

    try {
      const response = await this.openai.chat.completions.create({
        model: OPENAI_GPT_MODEL,
        messages: [
          {
            role: 'system',
            content: systemPrompt
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        response_format: { type: 'json_object' }
      })

      const content = response.choices[0]?.message?.content
      if (!content) {
        throw new Error('No response from OpenAI')
      }

      const result = JSON.parse(content)
      const fields = result.fields || []

      return this.mapToFormFields(fields)
    } catch (error) {
      console.error('Error generating additional fields:', error)
      throw new Error('Failed to generate additional fields')
    }
  }

  async generateFormLogic(fields: any[], prompt: string): Promise<any[]> {
    if (!this.openai) {
      throw new Error('OpenAI API is not configured')
    }

    const systemPrompt = `You are a form logic builder. Based on the form fields and user's request, generate conditional logic rules. Return a JSON array of logic rules.
    
Available fields: ${JSON.stringify(fields.map(f => ({ id: f.id, title: f.title, kind: f.kind })))}`

    try {
      const response = await this.openai.chat.completions.create({
        model: OPENAI_GPT_MODEL,
        messages: [
          {
            role: 'system',
            content: systemPrompt
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        response_format: { type: 'json_object' }
      })

      const content = response.choices[0]?.message?.content
      if (!content) {
        throw new Error('No response from OpenAI')
      }

      const result = JSON.parse(content)
      return result.logics || []
    } catch (error) {
      console.error('Error generating form logic:', error)
      throw new Error('Failed to generate form logic')
    }
  }

  private buildFormGenerationPrompt(topic: string, reference?: string): string {
    let prompt = `Generate form fields for: ${topic}\n\n`

    if (reference) {
      prompt += `Additional context and requirements:\n${reference}\n\n`
    }

    prompt += `Requirements:
- Generate appropriate form fields based on the topic
- Use proper field types (SHORT_TEXT, LONG_TEXT, EMAIL, PHONE_NUMBER, NUMBER, MULTIPLE_CHOICE, CHECKBOX, DATE, FILE_UPLOAD, etc.)
- Add helpful descriptions where appropriate
- Mark important fields as required
- For choice fields, provide relevant options
- Include a THANK_YOU field at the end

Return a JSON object with a "fields" array containing the form fields. Each field should have:
- title: The field label (as an array with the text)
- description: Optional field description (as an array with the text)
- kind: The field type (use exact enum values like SHORT_TEXT, LONG_TEXT, EMAIL, etc.)
- validations: Object with validation rules
- properties: Object with field-specific properties (like choices for MULTIPLE_CHOICE)`

    return prompt
  }

  private mapToFormFields(aiFields: any[]): GeneratedField[] {
    const fields: GeneratedField[] = []

    for (const field of aiFields) {
      const mappedField: GeneratedField = {
        id: nanoid(12),
        title: Array.isArray(field.title) ? field.title : [field.title || 'Untitled'],
        kind: this.mapFieldKind(field.kind || field.type)
      }

      if (field.description) {
        mappedField.description = Array.isArray(field.description)
          ? field.description
          : [field.description]
      }

      if (field.validations) {
        mappedField.validations = field.validations
      }

      if (field.properties) {
        mappedField.properties = field.properties
      }

      // Handle choice fields
      const choiceFieldTypes = [
        'MULTIPLE_CHOICE',
        'multiple_choice',
        'CHECKBOX',
        'DROPDOWN',
        'custom_checkbox',
        'dropdown'
      ]
      if (choiceFieldTypes.includes(field.kind) && field.choices) {
        mappedField.properties = {
          ...mappedField.properties,
          choices: field.choices.map((choice: any, index: number) => ({
            id: nanoid(12),
            label: typeof choice === 'string' ? choice : choice.label
          }))
        }
      }

      fields.push(mappedField)
    }

    // Always add a thank you field if not present
    const hasThankYou = fields.some(f => f.kind === FieldKindEnum.THANK_YOU)
    if (!hasThankYou) {
      fields.push({
        id: nanoid(12),
        title: ['Thank you!'],
        description: ['Thanks for completing this form. We appreciate your response.'],
        kind: FieldKindEnum.THANK_YOU
      })
    }

    return fields
  }

  private mapFieldKind(kind: string): FieldKindEnum {
    const kindMap: Record<string, FieldKindEnum> = {
      SHORT_TEXT: FieldKindEnum.SHORT_TEXT,
      LONG_TEXT: FieldKindEnum.LONG_TEXT,
      EMAIL: FieldKindEnum.EMAIL,
      PHONE_NUMBER: FieldKindEnum.PHONE_NUMBER,
      NUMBER: FieldKindEnum.NUMBER,
      MULTIPLE_CHOICE: FieldKindEnum.MULTIPLE_CHOICE,
      CHECKBOX: FieldKindEnum.MULTIPLE_CHOICE,
      DROPDOWN: FieldKindEnum.MULTIPLE_CHOICE,
      DATE: FieldKindEnum.DATE,
      TIME: FieldKindEnum.TIME,
      FILE_UPLOAD: FieldKindEnum.FILE_UPLOAD,
      RATING: FieldKindEnum.RATING,
      YES_NO: FieldKindEnum.YES_NO,
      URL: FieldKindEnum.URL,
      LEGAL_TERMS: FieldKindEnum.LEGAL_TERMS,
      SIGNATURE: FieldKindEnum.SIGNATURE,
      THANK_YOU: FieldKindEnum.THANK_YOU,
      WELCOME: FieldKindEnum.WELCOME,
      STATEMENT: FieldKindEnum.STATEMENT
    }

    return kindMap[kind] || FieldKindEnum.SHORT_TEXT
  }
}
