import { BadRequestException } from '@nestjs/common'

import { Auth, Project, ProjectGuard, Team, User } from '@decorator'
import { ProjectDetailInput } from '@graphql'
import { ProjectModel, TeamModel, UserModel } from '@model'
import { Args, Query, Resolver } from '@nestjs/graphql'

@Resolver()
@Auth()
export class DeleteProjectCodeResolver {
  constructor() {}

  @ProjectGuard()
  @Query(returns => Boolean)
  async deleteProjectCode(
    @Team() team: TeamModel,
    @Project() project: ProjectModel,
    @User() user: UserModel,
    @Args('input') input: ProjectDetailInput
  ): Promise<boolean> {
    if (!team.isOwner) {
      throw new BadRequestException("You don't have permission to delete the project")
    }

    // No longer sending email verification codes
    // Just return true to maintain API compatibility
    return true
  }
}
