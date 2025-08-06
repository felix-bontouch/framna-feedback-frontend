import { FieldKindEnum } from '@heyform-inc/shared-types-enums'
import { Injectable } from '@nestjs/common'
import OpenAI from 'openai'

import { OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_GPT_MODEL } from '@environments'
import { nanoid } from '@heyform-inc/utils'

import { AI_TOOLS } from './ai-tools'

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

interface LogicAnalysis {
  isLogicNeeded: boolean
  complexity: 'simple' | 'moderate' | 'complex'
  reasoning: string
  logicSuggestions?: string[]
}

interface FormGenerationResponse {
  fields: GeneratedField[]
  logicAnalysis: LogicAnalysis
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

  async generateFormFields(topic: string, reference?: string): Promise<FormGenerationResponse> {
    if (!this.openai) {
      throw new Error('OpenAI API is not configured')
    }

    const prompt = this.buildFormGenerationPrompt(topic, reference)

    try {
      console.log(
        'Calling OpenAI with tools:',
        JSON.stringify(AI_TOOLS.generateFormFields, null, 2)
      )

      const response = await this.openai.chat.completions.create({
        model: OPENAI_GPT_MODEL,
        messages: [
          {
            role: 'system',
            content: this.getProfessionalFormDesignerPrompt()
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        tools: [AI_TOOLS.generateFormFields],
        tool_choice: { type: 'function', function: { name: 'generate_form_fields' } }
      })

      // Extract the tool call
      const message = response.choices[0]?.message

      if (!message?.tool_calls?.length) {
        throw new Error('Expected function call in response')
      }

      const toolCall = message.tool_calls[0]
      if (toolCall.function.name !== 'generate_form_fields') {
        throw new Error('Expected generate_form_fields tool call')
      }

      const result = JSON.parse(toolCall.function.arguments)
      console.log('AI generation result:', JSON.stringify(result, null, 2))
      const fields = result.fields || []
      const logicAnalysis = result.logicAnalysis || {
        isLogicNeeded: false,
        complexity: 'simple',
        reasoning: 'Logic analysis not provided'
      }

      return {
        fields: this.mapToFormFields(fields),
        logicAnalysis
      }
    } catch (error) {
      console.error('Error generating form fields:', error)
      throw new Error('Failed to generate form fields')
    }
  }

  async generateAdditionalFields(existingFields: any[], prompt: string): Promise<GeneratedField[]> {
    if (!this.openai) {
      throw new Error('OpenAI API is not configured')
    }

    const existingFieldsInfo = JSON.stringify(
      existingFields.map(f => ({
        title: f.title,
        kind: f.kind,
        properties: f.properties
      }))
    )

    const systemPrompt = `${this.getProfessionalFormDesignerPrompt()}

Current form structure:
${existingFieldsInfo}

Based on the existing form fields and maintaining consistency with the current design, generate additional fields that:
1. Complement and enhance the existing form
2. Maintain logical flow and grouping
3. Avoid duplication of existing questions
4. Follow the same professional standards
5. Consider skip logic opportunities with existing fields`

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
        tools: [AI_TOOLS.generateAdditionalFields],
        tool_choice: { type: 'function', function: { name: 'generate_additional_fields' } }
      })

      // Extract the tool call
      const message = response.choices[0]?.message
      if (!message?.tool_calls?.length) {
        throw new Error('Expected function call in response')
      }

      const toolCall = message.tool_calls[0]
      if (toolCall.function.name !== 'generate_additional_fields') {
        throw new Error('Expected generate_additional_fields tool call')
      }

      const result = JSON.parse(toolCall.function.arguments)
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

    const systemPrompt = this.getProfessionalLogicBuilderPrompt(fields)

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
        tools: [AI_TOOLS.generateFormLogic],
        tool_choice: { type: 'function', function: { name: 'generate_form_logic' } }
      })

      // Extract the tool call
      const message = response.choices[0]?.message
      if (!message?.tool_calls?.length) {
        throw new Error('Expected function call in response')
      }

      const toolCall = message.tool_calls[0]
      if (toolCall.function.name !== 'generate_form_logic') {
        throw new Error('Expected generate_form_logic tool call')
      }

      const result = JSON.parse(toolCall.function.arguments)
      console.log('AI logic generation result:', JSON.stringify(result, null, 2))
      return result.logics || []
    } catch (error) {
      console.error('Error generating form logic:', error)
      throw new Error('Failed to generate form logic')
    }
  }

  async generateInitialFormLogic(
    fields: GeneratedField[],
    topic: string,
    logicSuggestions?: string[]
  ): Promise<any[]> {
    if (!this.openai) {
      throw new Error('OpenAI API is not configured')
    }

    let prompt = `Based on the form topic "${topic}" and the generated fields, create intelligent conditional logic.`

    if (logicSuggestions && logicSuggestions.length > 0) {
      prompt += `\n\nThe form analysis identified these specific logic needs:\n`
      logicSuggestions.forEach((suggestion, index) => {
        prompt += `${index + 1}. ${suggestion}\n`
      })
      prompt += `\nImplement these suggestions as conditional logic rules.`
    } else {
      prompt += `\n\nAnalyze the fields and create logic rules that:
1. Implement skip patterns to show only relevant questions
2. Create branching paths based on qualifying answers
3. Add validation dependencies between related fields
4. Optimize the user journey through the form`
    }

    try {
      const response = await this.openai.chat.completions.create({
        model: OPENAI_GPT_MODEL,
        messages: [
          {
            role: 'system',
            content: this.getProfessionalLogicBuilderPrompt(fields)
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        tools: [AI_TOOLS.generateFormLogic],
        tool_choice: { type: 'function', function: { name: 'generate_form_logic' } }
      })

      // Extract the tool call
      const message = response.choices[0]?.message
      if (!message?.tool_calls?.length) {
        throw new Error('Expected function call in response')
      }

      const toolCall = message.tool_calls[0]
      if (toolCall.function.name !== 'generate_form_logic') {
        throw new Error('Expected generate_form_logic tool call')
      }

      const result = JSON.parse(toolCall.function.arguments)
      console.log('AI initial logic generation result:', JSON.stringify(result, null, 2))
      return this.mapToFormLogic(result.logics || [], fields)
    } catch (error) {
      console.error('Error generating initial form logic:', error)
      return [] // Return empty array instead of throwing to allow form creation without logic
    }
  }

  private buildFormGenerationPrompt(topic: string, reference?: string): string {
    let prompt = `Design a professional, high-quality form for: ${topic}\n\n`

    if (reference) {
      prompt += `Additional context and requirements:\n${reference}\n\n`
    }

    prompt += `Follow these professional form design principles:

1. STRUCTURE & FLOW:
   - Start with a clear purpose statement or welcome message
   - Group related questions into logical sections
   - Progress from easy/general to complex/specific questions
   - Use progressive disclosure for complex forms
   - End with a professional thank you message

2. QUESTION DESIGN:
   - Write clear, unambiguous questions
   - Avoid leading questions and bias
   - Use appropriate field types for data collection
   - Include helpful descriptions and examples
   - Consider accessibility and inclusive language

3. DATA QUALITY:
   - Mark truly essential fields as required
   - Add appropriate validation rules
   - Include data quality checks where relevant
   - Consider skip logic opportunities
   - Design for mobile-first experience

4. STATISTICAL CONSIDERATIONS:
   - Use validated scales (e.g., 5-point Likert) where appropriate
   - Ensure response options are mutually exclusive and exhaustive
   - Consider the analysis requirements for each question
   - Balance between data completeness and respondent burden

CRITICAL: After generating fields, analyze whether this form requires conditional logic.

Generate form fields with proper structure including:
- Clear, unambiguous question text
- Helpful descriptions where needed
- Appropriate field types (SHORT_TEXT, MULTIPLE_CHOICE, etc.)
- Validation rules that make sense
- Statistical purpose for data analysis
- Skip logic hints for conditional flow

Also provide a comprehensive logic analysis that includes:
- Whether conditional logic would enhance the form
- The complexity level (simple, moderate, or complex)
- Clear reasoning for your recommendation
- Specific logic suggestions if applicable

LOGIC ANALYSIS GUIDELINES:
- SIMPLE forms (no logic needed): Basic contact forms, simple feedback, newsletter signups
- MODERATE forms (some logic helpful): Forms with optional sections, satisfaction surveys with follow-ups
- COMPLEX forms (logic essential): Applications with eligibility criteria, multi-path assessments, role-based questionnaires

Consider:
1. Are there qualifying questions that determine eligibility?
2. Do certain answers make other questions irrelevant?
3. Would skip patterns significantly improve user experience?
4. Are there dependent validations between fields?`

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

      // Initialize properties with verticalAlignment (required by frontend)
      mappedField.properties = {
        verticalAlignment: true,
        ...(field.properties || {})
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
      // Check for choices in both field.choices (legacy) and field.properties.choices (current)
      const choices = field.choices || field.properties?.choices
      if (choiceFieldTypes.includes(field.kind) && choices) {
        mappedField.properties = {
          ...mappedField.properties,
          choices: choices.map((choice: any) => ({
            id: nanoid(12),
            label: typeof choice === 'string' ? choice : choice.label
          }))
        }
      }

      // Handle YES_NO fields specifically - they always need Yes/No choices
      if (mappedField.kind === FieldKindEnum.YES_NO) {
        mappedField.properties = {
          ...mappedField.properties,
          choices: [
            {
              id: nanoid(12),
              label: 'Yes'
            },
            {
              id: nanoid(12),
              label: 'No'
            }
          ]
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
        kind: FieldKindEnum.THANK_YOU,
        properties: {
          verticalAlignment: true
        }
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

  private getProfessionalFormDesignerPrompt(): string {
    return `You are an expert form designer and statistician with deep expertise in survey methodology, user experience design, and data collection best practices. Your role is to create professional, scientifically-valid forms that maximize response rates and data quality.

Core Competencies:
- Survey methodology and statistical sampling techniques
- Question design to minimize bias and maximize validity
- Logical flow and skip patterns for optimal user experience
- Data validation and quality control measures
- Accessibility and inclusive design principles
- Mobile-first responsive design
- GDPR and privacy compliance

Design Principles:
1. Start with clear objectives and purpose statement
2. Use progressive disclosure - gather basic info before detailed
3. Group related questions into logical sections
4. Implement appropriate validation for data quality
5. Create clear, unambiguous questions without bias
6. Consider cultural sensitivity and inclusivity
7. Optimize for completion rates and data quality
8. Design for analysis - consider how data will be used

Field Type Selection:
- SHORT_TEXT: Names, brief answers (max 100 chars)
- LONG_TEXT: Detailed responses, comments
- EMAIL: Email addresses with validation
- PHONE_NUMBER: Phone numbers with format validation
- NUMBER: Numeric data with min/max validation
- MULTIPLE_CHOICE: Single selection from options
- YES_NO: Binary choices
- RATING: Likert scales, satisfaction ratings
- DATE: Date selections with appropriate ranges
- FILE_UPLOAD: Document/image uploads
- STATEMENT: Information/instruction blocks
- WELCOME: Opening screen with instructions
- THANK_YOU: Closing screen with next steps

Always generate well-structured fields with proper formatting and appropriate field types.`
  }

  private getProfessionalLogicBuilderPrompt(fields: any[]): string {
    const fieldsInfo = JSON.stringify(
      fields.map(f => ({
        id: f.id,
        title: f.title,
        kind: f.kind,
        properties: f.properties
      }))
    )

    return `You are an expert in form logic design and conditional workflows. Create intelligent branching logic that enhances user experience and data quality.

Available fields: ${fieldsInfo}

Logic Design Principles:
1. SKIP LOGIC: Navigate users past irrelevant questions
   - If answer is "No" to qualifying question → skip to next section
   - If age < 18 → skip adult-only questions
   - If not applicable → skip detailed follow-ups

2. DISPLAY LOGIC: Show/hide questions conditionally
   - Show follow-up questions based on previous answers
   - Display confirmation fields for critical data
   - Show different paths based on user type

3. VALIDATION LOGIC: Ensure data consistency
   - Cross-field validation (e.g., end date > start date)
   - Conditional requirements (if X then Y is required)
   - Range checks based on other answers

4. BRANCHING PATHS: Create personalized journeys
   - Different question sets for different user types
   - Progressive profiling based on responses
   - Smart routing to relevant sections

Logic Structure:
- Each logic rule has a source fieldId that triggers it
- Payloads contain conditions and corresponding actions
- Conditions use comparison operators (is, is_not, contains, greater_than, etc.)
- Actions can navigate to other fields or calculate variables
- Multiple conditions can be defined for the same field

Comparison operators:
- Text: is, is_not, contains, does_not_contain, starts_with, ends_with
- Numbers: equal, not_equal, greater_than, less_than, greater_or_equal_than, less_or_equal_than
- Dates: is_before, is_after
- Common: is_empty, is_not_empty

Focus on creating logic that:
- Reduces respondent burden
- Maintains data quality
- Creates personalized experiences
- Handles edge cases gracefully`
  }

  private mapToFormLogic(aiLogics: any[], fields: GeneratedField[]): any[] {
    if (!aiLogics || !Array.isArray(aiLogics)) {
      return []
    }

    // Create a map of field titles to IDs for easy lookup
    const fieldMap = new Map(fields.map(f => [Array.isArray(f.title) ? f.title[0] : f.title, f.id]))

    return aiLogics
      .map(logic => {
        // Ensure fieldId exists
        const fieldId = logic.fieldId || fieldMap.get(logic.fieldTitle) || logic.sourceField
        if (!fieldId) return null

        return {
          fieldId,
          payloads: (logic.payloads || []).map((payload: any) => ({
            id: nanoid(12),
            condition: this.normalizeCondition(payload.condition),
            action: this.normalizeAction(payload.action, fieldMap)
          }))
        }
      })
      .filter(Boolean)
  }

  private normalizeCondition(condition: any): any {
    if (!condition) return { comparison: 'is', expected: '' }

    return {
      comparison: condition.comparison || 'is',
      expected: condition.expected !== undefined ? condition.expected : '',
      ref: condition.ref
    }
  }

  private normalizeAction(action: any, fieldMap: Map<string, string>): any {
    if (!action) return { kind: 'navigate', fieldId: '' }

    const normalized: any = {
      kind: action.kind || 'navigate'
    }

    if (action.kind === 'navigate') {
      normalized.fieldId =
        action.fieldId || fieldMap.get(action.fieldTitle) || action.targetField || ''
    } else if (action.kind === 'calculate') {
      normalized.variable = action.variable || ''
      normalized.operator = action.operator || 'assignment'
      normalized.value = action.value
      normalized.ref = action.ref
    }

    return normalized
  }
}
