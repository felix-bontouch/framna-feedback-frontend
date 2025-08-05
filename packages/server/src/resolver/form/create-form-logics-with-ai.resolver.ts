import { BadRequestException } from '@nestjs/common'

import { Auth, FormGuard, Team, User } from '@decorator'
import { CreateFieldsWithAIInput } from '@graphql'
import { TeamModel, UserModel } from '@model'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { AIService, FormService } from '@service'

@Resolver()
@Auth()
export class CreateFormLogicsWithAIResolver {
  constructor(
    private readonly formService: FormService,
    private readonly aiService: AIService
  ) {}

  @Mutation(returns => Boolean)
  @FormGuard()
  async createFormLogicsWithAI(
    @Team() team: TeamModel,
    @User() user: UserModel,
    @Args('input') input: CreateFieldsWithAIInput
  ): Promise<boolean> {
    try {
      // Get the current form
      const form = await this.formService.findById(input.formId)
      if (!form) {
        throw new BadRequestException('Form not found')
      }

      // Get current fields
      let fields = []
      try {
        fields = form._drafts ? JSON.parse(form._drafts) : []
      } catch (e) {
        fields = []
      }

      if (fields.length === 0) {
        throw new BadRequestException('No fields found in form')
      }

      // Generate logic using AI
      const generatedLogic = await this.aiService.generateFormLogic(fields, input.prompt)

      if (!generatedLogic || generatedLogic.length === 0) {
        throw new BadRequestException('No logic generated')
      }

      // Update the form with new logic
      await this.formService.update(form.id, {
        logics: generatedLogic,
        fieldsUpdatedAt: Date.now()
      })

      return true
    } catch (error) {
      console.error('Error creating form logic with AI:', error)
      throw new BadRequestException(error.message || 'Failed to create form logic with AI')
    }
  }
}
