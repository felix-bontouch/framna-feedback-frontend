import { useState } from 'react'
import { useTranslation } from 'react-i18next'

import { FormService } from '@/services'

import { useToast } from '@/components'
import { FormType } from '@/types'

interface UsePublishFormOptions {
  onSuccess?: () => void
  onError?: (error: Error) => void
}

export function usePublishForm(options?: UsePublishFormOptions) {
  const { t } = useTranslation()
  const toast = useToast()
  const [loading, setLoading] = useState(false)

  const publishForm = async (form: FormType) => {
    console.log('🔍 DEBUG: publishForm called with:', {
      formId: form?.id,
      hasDrafts: !!form?.drafts,
      draftsLength: form?.drafts?.length,
      version: form?.version,
      draftsType: typeof form?.drafts,
      firstDraft: form?.drafts?.[0],
      loading
    })

    if (loading) {
      console.log('⚠️ Already loading, skipping publish')
      return
    }

    setLoading(true)

    try {
      // Validate form has necessary data
      if (!form?.drafts || form?.version === undefined) {
        console.error('❌ Validation failed:', {
          hasDrafts: !!form?.drafts,
          drafts: form?.drafts,
          version: form?.version
        })
        throw new Error(
          t(
            'form.publish.error.noDrafts',
            'Form drafts not available. Please make sure the form has content.'
          )
        )
      }

      if (!form?.id) {
        console.error('❌ Form ID missing')
        throw new Error(t('form.publish.error.noId', 'Form ID is missing'))
      }

      console.log('✅ Validation passed, calling FormService.publishForm')

      // Use the proper publish method (sanitization is now handled in the service)
      const result = await FormService.publishForm({
        formId: form.id,
        version: form.version,
        drafts: form.drafts
      })

      console.log('✅ Publish successful:', result)

      // Show success message
      toast({
        title: t('form.publish.success.title', 'Success'),
        message: t('form.publish.success.message', 'Form has been published successfully')
      })

      // Call success callback if provided
      options?.onSuccess?.()

      return true
    } catch (err: any) {
      // Show error message to user
      console.error('Failed to publish form:', err)

      toast({
        title: t('form.publish.error.title', 'Failed to publish'),
        message:
          err.message ||
          t('form.publish.error.message', 'An error occurred while publishing the form')
      })

      // Call error callback if provided
      options?.onError?.(err)

      return false
    } finally {
      setLoading(false)
    }
  }

  return {
    publishForm,
    loading
  }
}
