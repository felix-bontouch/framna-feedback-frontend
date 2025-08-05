import { useTranslation } from 'react-i18next'

import { Form, Select, Switch } from '@/components'

export default function FormSettingsGeneral() {
  const { t } = useTranslation()

  const categoryOptions = [
    { value: 'GENERAL', label: 'General Feedback' },
    { value: 'NPS', label: 'Net Promoter Score (NPS)' },
    { value: 'FEATURE', label: 'Feature Specific' },
    { value: 'USER_FLOW', label: 'User Flow Feedback' },
    { value: 'PERFORMANCE', label: 'Performance Issues' },
    { value: 'ONBOARDING', label: 'Onboarding Experience' },
    { value: 'RATING', label: 'App Store Rating' }
  ]

  return (
    <section id="general">
      <h2 className="text-lg font-semibold">{t('form.settings.general.title')}</h2>

      <div className="mt-4 space-y-8">
        <Form.Item
          name="mobileCategory"
          label="Category"
          description="Categorize feedback to better organize and analyze responses"
          isInline
        >
          <Select
            className="w-full min-w-48 sm:w-auto"
            options={categoryOptions}
            placeholder="Select category"
          />
        </Form.Item>
        <Form.Item
          className="[&_[data-slot=content]]:pt-1.5"
          name="allowArchive"
          label={t('form.settings.general.archive.headline')}
          description={t('form.settings.general.archive.subHeadline')}
          isInline
        >
          <Switch />
        </Form.Item>

        <Form.Item
          className="[&_[data-slot=content]]:pt-1.5"
          name="enableProgress"
          label={t('form.settings.general.progressBar.headline')}
          description={t('form.settings.general.progressBar.subHeadline')}
          isInline
        >
          <Switch />
        </Form.Item>

        <Form.Item
          className="[&_[data-slot=content]]:pt-1.5"
          name="enableQuestionList"
          label={t('form.settings.general.viewQuestions.headline')}
          description={t('form.settings.general.viewQuestions.subHeadline')}
          isInline
        >
          <Switch />
        </Form.Item>

        <Form.Item
          className="[&_[data-slot=content]]:pt-1.5"
          name="enableNavigationArrows"
          label={t('form.settings.general.navigationArrows.headline')}
          description={t('form.settings.general.navigationArrows.subHeadline')}
          isInline
        >
          <Switch />
        </Form.Item>
      </div>
    </section>
  )
}
