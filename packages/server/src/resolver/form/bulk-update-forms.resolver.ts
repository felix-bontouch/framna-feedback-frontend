import { Auth, ProjectGuard } from '@decorator'
import { BulkUpdateFormsInput } from '@graphql'
import { helper } from '@heyform-inc/utils'
import { Args, Mutation, Resolver } from '@nestjs/graphql'
import { FormService, ProjectService } from '@service'

@Resolver()
@Auth()
export class BulkUpdateFormsResolver {
  constructor(
    private readonly formService: FormService,
    private readonly projectService: ProjectService
  ) {}

  @Mutation(returns => Boolean)
  @ProjectGuard()
  async bulkUpdateForms(@Args('input') input: BulkUpdateFormsInput): Promise<boolean> {
    // Verify all forms belong to the same project
    const forms = await this.formService.findAll(input.formIds, null)
    const projectIds = [...new Set(forms.map(f => f.projectId))]

    if (projectIds.length > 1) {
      throw new Error('All forms must belong to the same project')
    }

    const updates: Record<string, any> = {}

    // Handle status updates (active/inactive)
    if (helper.isBoolean(input.active)) {
      updates['settings.active'] = input.active
    }

    // Handle project move
    if (input.targetProjectId) {
      const targetProject = await this.projectService.findById(input.targetProjectId)
      if (!targetProject) {
        throw new Error('Target project not found')
      }
      updates.projectId = input.targetProjectId
    }

    // Handle settings updates
    if (input.enableClosedMessage !== undefined) {
      updates['settings.enableClosedMessage'] = input.enableClosedMessage
    }

    if (input.closedFormTitle) {
      updates['settings.closedFormTitle'] = input.closedFormTitle
    }

    if (input.closedFormDescription) {
      updates['settings.closedFormDescription'] = input.closedFormDescription
    }

    if (input.enableEmailNotification !== undefined) {
      updates['settings.enableEmailNotification'] = input.enableEmailNotification
    }

    if (input.requirePassword !== undefined) {
      updates['settings.requirePassword'] = input.requirePassword
    }

    if (input.password) {
      updates['settings.password'] = input.password
    }

    if (input.enableQuotaLimit !== undefined) {
      updates['settings.enableQuotaLimit'] = input.enableQuotaLimit
    }

    if (input.quotaLimit) {
      updates['settings.quotaLimit'] = input.quotaLimit
    }

    if (input.enableIpLimit !== undefined) {
      updates['settings.enableIpLimit'] = input.enableIpLimit
    }

    if (input.ipLimitCount) {
      updates['settings.ipLimitCount'] = input.ipLimitCount
    }

    if (input.locale) {
      updates['settings.locale'] = input.locale
    }

    if (helper.isValidArray(input.languages)) {
      updates['settings.languages'] = input.languages
    }

    // Update all forms
    return this.formService.updateMany(input.formIds, updates)
  }
}
