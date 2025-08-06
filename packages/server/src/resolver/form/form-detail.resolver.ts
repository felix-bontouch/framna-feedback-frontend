import { Auth, FormGuard, Team } from '@decorator'
import { FormDetailInput, FormType, MobileFormType, PublicFormType } from '@graphql'
import { date } from '@heyform-inc/utils'
import { TeamModel } from '@model'
import { Args, Query, Resolver } from '@nestjs/graphql'
import { FormService, MobileTransformerService, SubmissionService } from '@service'

@Resolver()
@Auth()
export class FormDetailResolver {
  constructor(
    private readonly formService: FormService,
    private readonly submissionService: SubmissionService,
    private readonly mobileTransformerService: MobileTransformerService
  ) {}

  @Query(returns => FormType)
  @FormGuard()
  async formDetail(@Team() team: TeamModel, @Args('input') input: FormDetailInput): Promise<any> {
    const [form, submissionCount] = await Promise.all([
      this.formService.findById(input.formId),
      this.submissionService.count({ formId: input.formId })
    ])

    // Convert to plain object to ensure virtual fields are included
    const formObject: any = form.toObject({ virtuals: true })

    // Add computed fields
    formObject.updatedAt = date(form.get('updatedAt')).unix()
    formObject.submissionCount = submissionCount

    // Debug logging for AI forms
    console.log('🔍 DEBUG: formDetail response for', input.formId, {
      hasDrafts: !!formObject.drafts,
      draftsLength: formObject.drafts?.length,
      hasFields: !!formObject.fields,
      fieldsLength: formObject.fields?.length,
      version: formObject.version,
      canPublish: formObject.canPublish,
      isDraft: formObject.isDraft,
      has_drafts: !!form._drafts,
      _draftsLength: form._drafts?.length
    })

    return formObject
  }

  @Query(returns => PublicFormType)
  async publicForm(
    @Args('input') input: FormDetailInput
  ): Promise<PublicFormType | MobileFormType> {
    const form = await this.formService.findPublicForm(input.formId)

    if (!form) {
      throw new Error('Form not found')
    }

    if (!form.teamId) {
      throw new Error('Form teamId is required')
    }

    if (!form.projectId) {
      throw new Error('Form projectId is required')
    }

    // Check if mobile platform is requested
    if (input.platform === 'mobile') {
      return this.mobileTransformerService.transformFormForMobile(form)
    }

    // Default web response with all theme and visual data
    const integrations: Record<string, any> = {}

    if (form.settings?.active) {
      // const apps = await this.appService.findAllByUniqueIds(['googleanalytics', 'facebookpixel'])
      // const result = await this.integrationService.findAllInFormByApps(
      //   input.formId,
      //   apps.map(app => app.id)
      // )
      // for (const row of result) {
      //   const app = apps.find(app => app.id === row.appId)
      //   integrations[app.uniqueId] = (row.attributes as any).get('trackingCode')
      // }
    }

    return {
      id: form.id,
      teamId: form.teamId,
      projectId: form.projectId,
      memberId: form.memberId,
      name: form.name,
      description: form.description,
      interactiveMode: form.interactiveMode,
      kind: form.kind,
      settings: form.settings,
      drafts: form.drafts || form.fields || [],
      fields: form.fields || [],
      translations: form.translations || {},
      hiddenFields: form.hiddenFields || [],
      logics: form.logics || [],
      variables: form.variables || [],
      fieldsUpdatedAt: form.fieldsUpdatedAt || Date.now(),
      themeSettings: form.themeSettings || {},
      retentionAt: form.retentionAt,
      suspended: form.suspended || false,
      isDraft: form.isDraft || false,
      status: form.status,
      version: form.version || 1,
      canPublish: form.canPublish || false,
      customReport: form.customReport || {
        id: '',
        hiddenFields: [],
        theme: {},
        enablePublicAccess: false
      },
      integrations
    }
  }
}
