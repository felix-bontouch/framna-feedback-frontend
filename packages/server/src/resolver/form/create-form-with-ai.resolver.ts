import {
  CaptchaKindEnum,
  FormKindEnum,
  FormStatusEnum,
  InteractiveModeEnum
} from '@heyform-inc/shared-types-enums'
import { BadRequestException } from '@nestjs/common'

import { Auth, ProjectGuard, Team, User } from '@decorator'
import { CreateFormWithAIInput } from '@graphql'
import { TeamModel, UserModel } from '@model'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { AIService, FormService } from '@service'

@Resolver()
@Auth()
export class CreateFormWithAIResolver {
  constructor(
    private readonly formService: FormService,
    private readonly aiService: AIService
  ) {}
  @Mutation(() => String)
  @ProjectGuard()
  async createFormWithAI(
    @Team() team: TeamModel,
    @User() user: UserModel,
    @Args('input') input: CreateFormWithAIInput
  ): Promise<string> {
    console.log('🔍 DEBUG: createFormWithAI called', {
      teamId: team?.id,
      userId: user?.id,
      projectId: input?.projectId,
      topic: input?.topic,
      hasReference: !!input?.reference
    })

    try {
      // Generate form fields with logic analysis
      console.log('🔍 DEBUG: Calling AI service to generate fields...')
      const generationResult = await this.aiService.generateFormFields(input.topic, input.reference)

      console.log('🔍 DEBUG: AI generation result', {
        fieldsCount: generationResult?.fields?.length,
        hasLogicAnalysis: !!generationResult?.logicAnalysis,
        isLogicNeeded: generationResult?.logicAnalysis?.isLogicNeeded
      })

      if (!generationResult?.fields || generationResult.fields.length === 0) {
        throw new BadRequestException('Failed to generate form fields')
      }

      // Only generate logic if the AI determines it's needed
      let generatedLogic = []
      if (generationResult.logicAnalysis?.isLogicNeeded) {
        console.log(
          `Form requires logic (${generationResult.logicAnalysis.complexity}): ${generationResult.logicAnalysis.reasoning}`
        )

        generatedLogic = await this.aiService.generateInitialFormLogic(
          generationResult.fields,
          input.topic,
          generationResult.logicAnalysis.logicSuggestions
        )
      } else {
        console.log(`Form does not require logic: ${generationResult.logicAnalysis?.reasoning}`)
      }

      // Determine the most appropriate form kind based on the topic
      const formKind = this.determineFormKind(input.topic)

      // Create form with generated fields and logic
      console.log('🔍 DEBUG: Creating form with:', {
        formKind,
        fieldsCount: generationResult.fields.length,
        logicsCount: generatedLogic.length
      })

      const formId = await this.formService.create({
        teamId: team.id,
        memberId: user.id,
        projectId: input.projectId,
        name: this.generateFormName(input.topic),
        description: `AI-generated form for: ${input.topic}`,
        interactiveMode: InteractiveModeEnum.INTERACTIVE,
        kind: formKind,
        fields: [],
        _drafts: JSON.stringify(generationResult.fields),
        logics: generatedLogic,
        fieldsUpdatedAt: Date.now(),
        settings: {
          active: false,
          captchaKind: CaptchaKindEnum.NONE,
          filterSpam: true,
          allowArchive: true,
          requirePassword: false,
          locale: 'en',
          enableQuestionList: true,
          enableNavigationArrows: true,
          enableEmailNotification: true,
          enableProgress: true,
          mobileCategory: this.determineMobileCategory(input.topic)
        },
        hiddenFields: [],
        version: 0,
        status: FormStatusEnum.NORMAL
      })

      console.log('🔍 DEBUG: Form created successfully with ID:', formId)

      return formId
    } catch (error) {
      console.error('❌ DEBUG: Error creating form with AI:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      })
      throw new BadRequestException(error.message || 'Failed to create form with AI')
    }
  }
  private generateFormName(topic: string): string {
    // Clean up the topic to create a form name
    const cleanTopic = topic
      .replace(/create\s+a?\s*/i, '')
      .replace(/form\s+for\s*/i, '')
      .replace(/form\s+to\s*/i, '')
      .trim()
    // Capitalize first letter
    const name = cleanTopic.charAt(0).toUpperCase() + cleanTopic.slice(1)
    // Limit length
    if (name.length > 50) {
      return name.substring(0, 47) + '...'
    }

    return name
  }

  private determineFormKind(topic: string): FormKindEnum {
    const lowerTopic = topic.toLowerCase()

    if (
      lowerTopic.includes('quiz') ||
      lowerTopic.includes('test') ||
      lowerTopic.includes('assessment')
    ) {
      return FormKindEnum.QUIZ
    }

    if (
      lowerTopic.includes('contact') ||
      lowerTopic.includes('inquiry') ||
      lowerTopic.includes('support')
    ) {
      return FormKindEnum.CONTACT
    }

    // Default to survey for most forms
    return FormKindEnum.SURVEY
  }

  private determineMobileCategory(topic: string): string {
    const lowerTopic = topic.toLowerCase()

    if (lowerTopic.includes('nps') || lowerTopic.includes('net promoter')) {
      return 'NPS'
    }

    if (lowerTopic.includes('feature') || lowerTopic.includes('product')) {
      return 'FEATURE'
    }

    if (lowerTopic.includes('onboarding') || lowerTopic.includes('welcome')) {
      return 'ONBOARDING'
    }

    if (
      lowerTopic.includes('rating') ||
      lowerTopic.includes('review') ||
      lowerTopic.includes('feedback')
    ) {
      return 'RATING'
    }

    if (lowerTopic.includes('performance') || lowerTopic.includes('evaluation')) {
      return 'PERFORMANCE'
    }

    return 'GENERAL'
  }
}
