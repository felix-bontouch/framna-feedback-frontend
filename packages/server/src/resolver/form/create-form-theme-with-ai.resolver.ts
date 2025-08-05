import { BadRequestException } from '@nestjs/common'

import { Auth, FormGuard, Team, User } from '@decorator'
import { CreateFormThemeWithAIInput } from '@graphql'
import { TeamModel, UserModel } from '@model'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { AIService, FormService } from '@service'

@Resolver()
@Auth()
export class CreateFormThemeWithAIResolver {
  constructor(
    private readonly formService: FormService,
    private readonly aiService: AIService
  ) {}

  @Mutation(returns => Boolean)
  @FormGuard()
  async createFormThemeWithAI(
    @Team() team: TeamModel,
    @User() user: UserModel,
    @Args('input') input: CreateFormThemeWithAIInput
  ): Promise<boolean> {
    try {
      // Get the current form
      const form = await this.formService.findById(input.formId)
      if (!form) {
        throw new BadRequestException('Form not found')
      }

      // Generate theme using AI
      const generatedTheme = await this.aiService.generateFormTheme(input.theme, input.prompt)

      if (!generatedTheme) {
        throw new BadRequestException('Failed to generate theme')
      }

      // Update the form with new theme
      await this.formService.update(form.id, {
        themeSettings: {
          theme: generatedTheme
        }
      })

      return true
    } catch (error) {
      console.error('Error creating form theme with AI:', error)
      throw new BadRequestException(error.message || 'Failed to create form theme with AI')
    }
  }
}
