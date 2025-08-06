import { IconEye, IconSend2 } from '@tabler/icons-react'
import { observer } from 'mobx-react-lite'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'

import { FormService } from '@/services'

import { Button, Tooltip } from '@/components'
import { usePublishForm } from '@/hooks'
import { useAppStore, useFormStore } from '@/store'

export const FormActions = observer(() => {
  const { t } = useTranslation()

  const appStore = useAppStore()
  const formStore = useFormStore()
  const [isLoadingDrafts, setIsLoadingDrafts] = useState(false)

  const { publishForm, loading } = usePublishForm({
    onSuccess: () => {
      // Update local state to reflect published status
      formStore.updateForm({
        canPublish: false,
        settings: {
          ...formStore.form?.settings,
          active: true
        }
      })
    }
  })

  // Ensure form has drafts loaded
  useEffect(() => {
    if (formStore.form && !formStore.form.drafts && formStore.form.id) {
      setIsLoadingDrafts(true)
      // Fetch full form details if drafts are missing
      FormService.detail(formStore.form.id)
        .then(fullForm => {
          formStore.setForm(fullForm)
        })
        .catch(err => {
          console.error('Failed to load form details:', err)
        })
        .finally(() => {
          setIsLoadingDrafts(false)
        })
    }
  }, [formStore.form?.id])

  const handlePreview = useCallback(() => {
    appStore.openModal('isFormPreviewOpen')
  }, [appStore])

  const handlePublish = useCallback(async () => {
    console.log('🔍 DEBUG: handlePublish called with form:', {
      formId: formStore.form?.id,
      hasForm: !!formStore.form,
      hasDrafts: !!formStore.form?.drafts,
      draftsLength: formStore.form?.drafts?.length,
      version: formStore.form?.version,
      canPublish: formStore.form?.canPublish,
      isActive: formStore.form?.settings?.active,
      fields: formStore.form?.fields?.length || 0,
      firstDraft: formStore.form?.drafts?.[0]
    })

    if (formStore.form) {
      await publishForm(formStore.form)
    } else {
      console.error('❌ No form available to publish')
    }
  }, [formStore.form, publishForm])

  const publishDisabled =
    formStore.form?.settings?.active || !formStore.form?.canPublish || isLoadingDrafts
  const publishTooltip = useMemo(() => {
    if (formStore.form?.settings?.active) {
      return t('form.publish.tooltip.alreadyPublished', 'Form is already published')
    }
    if (!formStore.form?.canPublish) {
      return t('form.publish.tooltip.noChanges', 'No changes to publish')
    }
    if (isLoadingDrafts) {
      return t('form.publish.tooltip.loading', 'Loading form content...')
    }
    return null
  }, [formStore.form?.settings?.active, formStore.form?.canPublish, isLoadingDrafts, t])

  const actions = useMemo(
    () => [
      {
        label: t('form.preview'),
        icon: IconEye,
        onClick: handlePreview
      },
      {
        label: formStore.form?.settings?.active ? t('form.published') : t('form.publish'),
        icon: IconSend2,
        disabled: publishDisabled,
        onClick: handlePublish,
        tooltip: publishTooltip
      }
    ],
    [
      t,
      publishDisabled,
      publishTooltip,
      handlePreview,
      handlePublish,
      formStore.form?.settings?.active
    ]
  )

  return (
    <div className="flex flex-col items-center gap-2.5 md:mr-3 md:flex-row md:gap-1">
      {actions.map((action, index) => {
        const button = (
          <Button.Link
            key={index}
            className="!flex w-full items-center !justify-start gap-3 !px-0 !py-1 !text-sm md:w-auto md:flex-col md:!justify-center md:gap-0 md:!px-1.5 md:!text-xs"
            disabled={action.disabled}
            onClick={action.onClick}
            loading={index === 1 && (loading || isLoadingDrafts)}
          >
            {action.label}
          </Button.Link>
        )

        if (action.tooltip) {
          return (
            <Tooltip key={index} label={action.tooltip}>
              {button}
            </Tooltip>
          )
        }

        return button
      })}
    </div>
  )
})
