import { CaptchaKindEnum, FieldKindEnum, FormStatusEnum } from '@heyform-inc/shared-types-enums'

import { Auth, ProjectGuard, Team, User } from '@decorator'
import { CreateFormInput } from '@graphql'
import { nanoid } from '@heyform-inc/utils'
import { TeamModel, UserModel } from '@model'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { FormService } from '@service'

@Resolver()
@Auth()
export class CreateFormResolver {
  constructor(private readonly formService: FormService) {}

  @Mutation(returns => String)
  @ProjectGuard()
  async createForm(
    @Team() team: TeamModel,
    @User() user: UserModel,
    @Args('input') input: CreateFormInput
  ): Promise<string> {
    const fields = [
      {
        id: nanoid(12),
        title: null,
        description: null,
        kind: FieldKindEnum.SHORT_TEXT,
        validations: { required: false }
      },
      {
        id: nanoid(12),
        title: ['Thank you!'],
        description: ['Thanks for completing this form. Now create your own form.'],
        kind: FieldKindEnum.THANK_YOU
      }
    ]

    return await this.formService.create({
      teamId: team.id,
      memberId: user.id,
      fields: [],
      _drafts: JSON.stringify(fields),
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
      hiddenFields: [],
      version: 0,
      status: FormStatusEnum.NORMAL,
      ...input
    })
  }
}
