import { BadRequestException } from '@nestjs/common'

import { Auth, FormGuard, Team, User } from '@decorator'
import { CreateFieldsWithAIInput } from '@graphql'
import { TeamModel, UserModel } from '@model'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { AIService, FormService } from '@service'

@Resolver()
@Auth()
export class CreateFieldsWithAIResolver {
  constructor(
    private readonly formService: FormService,
    private readonly aiService: AIService
  ) {}

  @Mutation(returns => Boolean)
  @FormGuard()
  async createFieldsWithAI(
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

      // Parse existing drafts
      let existingDrafts = []
      try {
        existingDrafts = form._drafts ? JSON.parse(form._drafts) : []
      } catch (e) {
        existingDrafts = []
      }

      // Generate additional fields using AI
      const newFields = await this.aiService.generateAdditionalFields(existingDrafts, input.prompt)

      if (!newFields || newFields.length === 0) {
        throw new BadRequestException('No fields generated')
      }

      // Remove thank you field from existing drafts if present (we'll add it at the end)
      const fieldsWithoutThankYou = existingDrafts.filter((f: any) => f.kind !== 'thank_you')

      // Find the thank you field or create a new one
      const thankYouField =
        existingDrafts.find((f: any) => f.kind === 'thank_you') ||
        newFields.find(f => f.kind === 'thank_you')

      // Remove thank you from new fields if present
      const newFieldsWithoutThankYou = newFields.filter(f => f.kind !== 'thank_you')

      // Combine fields with thank you at the end
      const updatedDrafts = [...fieldsWithoutThankYou, ...newFieldsWithoutThankYou]
      if (thankYouField) {
        updatedDrafts.push(thankYouField)
      }

      // Update the form
      await this.formService.update(form.id, {
        _drafts: JSON.stringify(updatedDrafts),
        fieldsUpdatedAt: Date.now()
      })

      return true
    } catch (error) {
      console.error('Error creating fields with AI:', error)
      throw new BadRequestException(error.message || 'Failed to create fields with AI')
    }
  }
}
