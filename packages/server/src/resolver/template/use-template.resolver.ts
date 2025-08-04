import { CaptchaKindEnum, FormStatusEnum } from '@heyform-inc/shared-types-enums'
import { BadRequestException } from '@nestjs/common'

import { Auth, ProjectGuard, Team, User } from '@decorator'
import { UseTemplateInput } from '@graphql'
import { helper } from '@heyform-inc/utils'
import { TeamModel, UserModel } from '@model'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { FormService } from '@service'

@Resolver()
@Auth()
export class UseTemplateResolver {
  constructor(private readonly formService: FormService) {}

  @Mutation(returns => String)
  @ProjectGuard()
  async useTemplate(
    @Team() team: TeamModel,
    @User() user: UserModel,
    @Args('input') input: UseTemplateInput
  ): Promise<string> {
    const template = await this.formService.findById(input.templateId)

    if (helper.isEmpty(template)) {
      throw new BadRequestException('The template does not exist')
    }

    const form = {
      teamId: team.id,
      projectId: input.projectId,
      memberId: user.id,
      name: template.name,
      kind: template.kind,
      interactiveMode: template.interactiveMode,
      fields: [],
      _drafts: JSON.stringify(template.fields),
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
        enableEmailNotification: true
      },
      themeSettings: template.themeSettings,
      hiddenFields: [],
      version: 0,
      status: FormStatusEnum.NORMAL
    }

    return this.formService.create(form)
  }
}
