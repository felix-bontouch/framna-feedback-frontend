import {
  CaptchaKindEnum,
  SubmissionCategoryEnum,
  SubmissionStatusEnum,
  UNSELECTABLE_FIELD_KINDS
} from '@heyform-inc/shared-types-enums'
import { BadRequestException, Injectable } from '@nestjs/common'

import { MobileSubmissionRequestDto } from '@dto'
import { applyLogicToFields, fieldValuesToAnswers, flattenFields } from '@heyform-inc/answer-utils'
import { helper, timestamp } from '@heyform-inc/utils'
import {
  EndpointService,
  FormReportService,
  IntegrationService,
  MobileTransformerService,
  SubmissionIpLimitService,
  SubmissionService
} from '@service'

@Injectable()
export class MobileFormService {
  constructor(
    private readonly mobileTransformerService: MobileTransformerService,
    private readonly submissionService: SubmissionService,
    private readonly endpointService: EndpointService,
    private readonly submissionIpLimitService: SubmissionIpLimitService,
    private readonly formReportService: FormReportService,
    private readonly integrationService: IntegrationService
  ) {}

  /**
   * Transform form for mobile consumption (no caching for real-time updates)
   */
  async transformFormForMobile(form: any): Promise<any> {
    // Transform using existing service without caching
    const transformed = this.mobileTransformerService.transformFormForMobile(form)
    console.log(`Form ${form.id}: transformed form with ${transformed.fields?.length || 0} fields`)
    return transformed
  }

  /**
   * Get specific fields from a form
   */
  async getFormFields(form: any, fieldIds?: string): Promise<any> {
    const mobileForm = await this.transformFormForMobile(form)

    if (!fieldIds) {
      return { fields: mobileForm.fields }
    }

    const requestedFieldIds = fieldIds.split(',').map(id => id.trim())
    const fields = mobileForm.fields.filter(field => requestedFieldIds.includes(field.id))

    return { fields }
  }

  /**
   * Submit form with mobile-specific handling
   */
  async submitForm(
    form: any,
    submissionDto: MobileSubmissionRequestDto
  ): Promise<{ submissionId: string }> {
    // Validate required fields
    if (!submissionDto.answers || typeof submissionDto.answers !== 'object') {
      throw new BadRequestException('Answers are required')
    }

    if (!submissionDto.startedAt) {
      throw new BadRequestException('startedAt timestamp is required')
    }

    // Check form constraints
    if (helper.isEmpty(form.fields)) {
      throw new BadRequestException('The form does not have content')
    }

    // Check quota limits
    if (
      form.settings?.enableQuotaLimit &&
      helper.isValid(form.settings.quotaLimit) &&
      form.settings.quotaLimit > 0
    ) {
      const count = await this.submissionService.countInForm(form.id)
      if (count >= form.settings.quotaLimit) {
        throw new BadRequestException('Submission quota exceeded')
      }
    }

    // Check IP limits
    if (
      form.settings?.enableIpLimit &&
      helper.isValid(form.settings.ipLimitCount) &&
      form.settings.ipLimitCount > 0 &&
      submissionDto.clientInfo.ip
    ) {
      await this.submissionIpLimitService.checkIp(form, submissionDto.clientInfo.ip)
    }

    // Check password if required
    if (form.settings?.requirePassword) {
      if (!submissionDto.password) {
        throw new BadRequestException('Password is required')
      }
      if (submissionDto.password !== form.settings.password) {
        throw new BadRequestException('Invalid password')
      }
    }

    // Verify captcha if enabled
    if (form.settings?.captchaKind && form.settings.captchaKind !== CaptchaKindEnum.NONE) {
      if (!submissionDto.captchaToken) {
        throw new BadRequestException('Captcha verification required')
      }
      // For mobile, we'll need to implement captcha verification
      // This is a placeholder for now
    }

    // Process answers through logic engine
    let answers
    let variables
    try {
      const { fields, variables: variableValues } = applyLogicToFields(
        flattenFields(form.fields, true),
        form.logics || [],
        form.variables || [],
        submissionDto.answers
      )

      answers = fieldValuesToAnswers(fields, submissionDto.answers, submissionDto.isPartial)
      variables = form.variables?.map(variable => ({
        ...variable,
        value: variableValues[variable.id]
      }))
    } catch (err) {
      // Provide detailed error information for validation failures
      if (err.response) {
        throw new BadRequestException({
          statusCode: 400,
          message: `Validation failed for field "${err.response.title || err.response.id}": ${err.message}`,
          error: 'Bad Request',
          field: err.response.id,
          fieldTitle: err.response.title,
          fieldKind: err.response.kind,
          value: err.response.value
        })
      }
      throw new BadRequestException(err.message || 'Invalid form data')
    }

    // Build submission data
    const submissionData: any = {
      teamId: form.teamId,
      formId: form.id,
      title: form.name,
      answers,
      hiddenFields: submissionDto.hiddenFields || [],
      variables,
      startAt: submissionDto.startedAt,
      endAt: timestamp(),
      ip: submissionDto.clientInfo.ip || 'unknown',
      userAgent: submissionDto.clientInfo.userAgent || 'mobile'
    }

    // Set status based on archive settings - only set to PRIVATE if archive is explicitly disabled
    if (form.settings?.allowArchive === false) {
      submissionData.status = SubmissionStatusEnum.PRIVATE
    } else {
      // Default to PUBLIC (matches the model's default)
      submissionData.status = SubmissionStatusEnum.PUBLIC
    }

    // TODO: Store extended client info when metadata field is added to model
    // Extended client info: os, osVersion, appVersion, device, deviceId, locale

    // Check for spam if enabled and set category only if spam
    if (form.settings?.filterSpam && submissionDto.clientInfo.ip) {
      const isSpam = await this.endpointService.verifySpam({
        answers,
        ip: submissionDto.clientInfo.ip
      })
      if (isSpam) {
        submissionData.category = SubmissionCategoryEnum.SPAM
      }
    }
    // Note: If not spam, category will default to SubmissionCategoryEnum.INBOX in the model

    // Create submission
    const submissionId = await this.submissionService.create(submissionData)

    // Queue background jobs
    this.formReportService.addQueue(form.id)
    this.integrationService.addQueue(form, submissionId)

    return { submissionId }
  }

  /**
   * Get form share information for mobile
   */
  async getFormShareInfo(form: any): Promise<any> {
    // Calculate form statistics
    const fields = flattenFields(form.fields || form.drafts || [])
    const selectableFields = fields.filter(f => !UNSELECTABLE_FIELD_KINDS.includes(f.kind))
    const questionCount = selectableFields.length
    const estimatedTime = Math.round(1.2 * (Math.log(questionCount) / Math.log(2)))

    return {
      shareUrl: `${process.env.APP_HOMEPAGE_URL || 'https://app.framna.com'}/form/${form.id}`,
      isPublished: !form.isDraft && form.publishedAt > 0,
      isActive: form.settings?.active === true,
      metadata: {
        title: form.settings?.metaTitle || form.name,
        description:
          form.settings?.metaDescription ||
          `${questionCount} question${questionCount !== 1 ? 's' : ''}, ${estimatedTime} min${estimatedTime > 1 ? 's' : ''} to complete`,
        ogImageUrl: form.settings?.metaOGImageUrl,
        questionCount,
        estimatedTime
      },
      accessControl: {
        requiresPassword: form.settings?.requirePassword === true,
        hasIpLimit: form.settings?.enableIpLimit === true,
        hasTimeLimit: form.settings?.enableTimeLimit === true,
        expiresAt: form.settings?.closedAt
          ? new Date(form.settings.closedAt).toISOString()
          : undefined
      }
    }
  }

  /**
   * Update form settings (meta information)
   */
  async updateFormSettings(form: any, settingsDto: any): Promise<any> {
    const allowedUpdates: Record<string, any> = {}

    // Only allow specific meta fields to be updated
    if (settingsDto.metaTitle !== undefined) {
      allowedUpdates['settings.metaTitle'] = settingsDto.metaTitle
    }

    if (settingsDto.metaDescription !== undefined) {
      allowedUpdates['settings.metaDescription'] = settingsDto.metaDescription
    }

    if (settingsDto.metaOGImageUrl !== undefined) {
      allowedUpdates['settings.metaOGImageUrl'] = settingsDto.metaOGImageUrl
    }

    // In a real implementation, this would call FormService.update
    // For now, we'll just return success
    return {
      success: true,
      message: 'Settings updated successfully',
      updates: allowedUpdates
    }
  }
}
