import { Injectable } from '@nestjs/common'

import { MobileFormType } from '@graphql'

@Injectable()
export class MobileTransformerService {
  /**
   * Transform a form for mobile consumption by stripping out visual/theme elements
   * while preserving all functional data needed for form rendering and logic
   */
  transformFormForMobile(form: any): MobileFormType {
    return {
      // Core identifiers
      id: form.id,
      teamId: form.teamId,
      projectId: form.projectId,
      memberId: form.memberId,

      // Basic form info
      name: form.name,
      description: form.description,
      interactiveMode: form.interactiveMode,
      kind: form.kind,

      // Functional settings (excluding theme-related settings)
      settings: this.transformSettingsForMobile(form.settings),

      // Form structure and logic
      fields: this.transformFieldsForMobile(form.fields || form._drafts || []),
      hiddenFields: form.hiddenFields || [],
      logics: form.logics || [],
      variables: form.variables || [],
      translations: form.translations || {},

      // Metadata
      fieldsUpdatedAt: form.fieldsUpdatedAt || Date.now(),
      retentionAt: form.retentionAt,
      suspended: form.suspended || false,
      isDraft: false,
      status: form.status,
      version: form.version || 1
    }
  }

  /**
   * Transform form settings by keeping only functional settings
   * and removing visual/theme related settings
   */
  private transformSettingsForMobile(settings: any): any {
    if (!settings) return {}

    // List of functional settings to keep
    const functionalSettings = [
      'captchaKind',
      'active',
      'enableExpirationDate',
      'expirationTimeZone',
      'enabledAt',
      'closedAt',
      'enableTimeLimit',
      'timeLimit',
      'filterSpam',
      'allowArchive',
      'requirePassword',
      'redirectOnCompletion',
      'redirectUrl',
      'redirectDelay',
      'enableQuotaLimit',
      'quotaLimit',
      'enableIpLimit',
      'ipLimitCount',
      'ipLimitTime',
      'enableProgress',
      'enableQuestionList',
      'enableNavigationArrows',
      'locale',
      'languages',
      'enableClosedMessage',
      'closedFormTitle',
      'closedFormDescription',
      'enableEmailNotification'
    ]

    const mobileSettings: any = {}

    // Copy only functional settings
    functionalSettings.forEach(key => {
      if (settings[key] !== undefined) {
        mobileSettings[key] = settings[key]
      }
    })

    return mobileSettings
  }

  /**
   * Transform fields by removing visual layout properties
   * while keeping all functional properties
   */
  private transformFieldsForMobile(fields: any[]): any[] {
    return fields.map(field => {
      const mobileField: any = {
        id: field.id,
        kind: field.kind,
        title: field.title,
        description: field.description,
        validations: field.validations,
        width: field.width,
        hide: field.hide,
        frozen: field.frozen
      }

      // Transform properties to remove visual elements
      if (field.properties) {
        mobileField.properties = this.transformPropertiesForMobile(field.properties, field.kind)
      }

      // Recursively transform nested fields (for GROUP fields)
      if (field.properties?.fields) {
        mobileField.properties.fields = this.transformFieldsForMobile(field.properties.fields)
      }

      return mobileField
    })
  }

  /**
   * Transform field properties by removing visual styling
   * while keeping functional properties
   */
  private transformPropertiesForMobile(properties: any, fieldKind: string): any {
    if (!properties) return {}

    // List of functional properties to keep (varies by field type)
    const functionalProperties = [
      // Button properties
      'showButton',
      'buttonText',
      'buttonLinkUrl',

      // Choice properties
      'choices',
      'allowOther',
      'allowMultiple',
      'other',
      'randomize',

      // Rating/scale properties
      'total',
      'start',
      'leftLabel',
      'centerLabel',
      'rightLabel',
      'hideMarks',

      // Country/phone properties
      'defaultCountryCode',

      // Date/time properties
      'format',
      'allowTime',
      'use12Hours',

      // Table properties
      'tableColumns',

      // Scoring properties
      'score',

      // Media properties (functional, not visual)
      'sourceUrl',

      // Redirect properties
      'redirectUrl',
      'redirectOnCompletion',
      'redirectDelay',

      // Group field properties
      'fields',

      // Other functional properties
      'badge',
      'placeholder'
    ]

    const mobileProperties: any = {}

    // Copy only functional properties
    functionalProperties.forEach(key => {
      if (properties[key] !== undefined) {
        mobileProperties[key] = properties[key]
      }
    })

    // Special handling for choices to ensure they don't include visual properties
    if (mobileProperties.choices) {
      mobileProperties.choices = mobileProperties.choices.map((choice: any) => ({
        id: choice.id,
        label: choice.label,
        score: choice.score,
        isExpected: choice.isExpected
        // Removed: image, color
      }))
    }

    return mobileProperties
  }
}
