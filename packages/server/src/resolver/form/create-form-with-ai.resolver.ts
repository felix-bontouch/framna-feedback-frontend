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

  @Mutation(returns => String)
  @ProjectGuard()
  async createFormWithAI(
    @Team() team: TeamModel,
    @User() user: UserModel,
    @Args('input') input: CreateFormWithAIInput
  ): Promise<string> {
    try {
      // Generate form fields using AI
      const generatedFields = await this.aiService.generateFormFields(input.topic, input.reference)

      if (!generatedFields || generatedFields.length === 0) {
        throw new BadRequestException('Failed to generate form fields')
      }

      // Create form with generated fields
      const formId = await this.formService.create({
        teamId: team.id,
        memberId: user.id,
        projectId: input.projectId,
        name: this.generateFormName(input.topic),
        description: `AI-generated form for: ${input.topic}`,
        interactiveMode: InteractiveModeEnum.INTERACTIVE,
        kind: FormKindEnum.SURVEY,
        fields: [],
        _drafts: JSON.stringify(generatedFields),
        fieldsUpdatedAt: 0,
        settings: {
          active: false,
          captchaKind: CaptchaKindEnum.NONE,
          filterSpam: false,
          allowArchive: true,
          requirePassword: false,
          locale: 'en',
          enableQuestionList: true,
          enableNavigationArrows: true,
          enableEmailNotification: true,
          mobileCategory: 'GENERAL'
        },
        hiddenFields: [],
        version: 0,
        status: FormStatusEnum.NORMAL
      })

      return formId
    } catch (error) {
      console.error('Error creating form with AI:', error)
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
}
