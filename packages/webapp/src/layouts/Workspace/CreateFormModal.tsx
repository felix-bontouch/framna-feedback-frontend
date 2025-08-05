import { FormKindEnum, InteractiveModeEnum } from '@heyform-inc/shared-types-enums'
import { IconPlus, IconStack2 } from '@tabler/icons-react'
import { useRequest } from 'ahooks'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'

import { FormService } from '@/services'
import { useParam, useRouter } from '@/utils'

import IconAI from '@/assets/ai.svg?react'
import { Button, Form, Input, Modal, Select } from '@/components'
import { useAppStore, useModal } from '@/store'

import CreateWithAIModel from './CreateWithAIModel'
import TemplatesModel from './TemplatesModel'

const FORM_TYPES = [
  {
    id: 'ai',
    headline: 'form.creation.ai.headline',
    subHeadline: 'form.creation.ai.subHeadline',
    icon: IconAI
  },
  {
    id: 'scratch',
    headline: 'form.creation.scratch.headline',
    subHeadline: 'form.creation.scratch.subHeadline',
    icon: IconPlus
  },
  {
    id: 'template',
    headline: 'form.creation.template.headline',
    subHeadline: 'form.creation.template.subHeadline',
    icon: IconStack2
  }
]

const CreateFormComponent = () => {
  const { t } = useTranslation()

  const router = useRouter()
  const { workspaceId, projectId } = useParam()
  const { closeModal } = useAppStore()
  const [rcForm] = Form.useForm()

  const [activeName, setActiveName] = useState<string>()
  const [showDetailsForm, setShowDetailsForm] = useState(false)

  const categoryOptions = [
    { value: 'GENERAL', label: 'General Feedback' },
    { value: 'NPS', label: 'Net Promoter Score (NPS)' },
    { value: 'FEATURE', label: 'Feature Specific' },
    { value: 'USER_FLOW', label: 'User Flow Feedback' },
    { value: 'PERFORMANCE', label: 'Performance Issues' },
    { value: 'ONBOARDING', label: 'Onboarding Experience' },
    { value: 'RATING', label: 'App Store Rating' }
  ]

  const { loading, run } = useRequest(
    async (values: any) => {
      const formId = await FormService.create({
        projectId,
        name: values.name || t('form.creation.defaultName'),
        nameSchema: [],
        interactiveMode: InteractiveModeEnum.GENERAL,
        kind: FormKindEnum.SURVEY,
        description: values.description,
        mobileCategory: values.mobileCategory
      })

      closeModal('CreateFormModal')
      router.push(`/workspace/${workspaceId}/project/${projectId}/form/${formId}/create`)
    },
    {
      refreshDeps: [projectId, t],
      manual: true
    }
  )

  function handleClick(name: string) {
    switch (name) {
      case 'scratch':
        setShowDetailsForm(true)
        break

      case 'ai':
        setActiveName(name)
        break

      default:
        setActiveName(name)
        break
    }
  }

  function handleBack() {
    setActiveName(undefined)
    setShowDetailsForm(false)
    rcForm.resetFields()
  }

  if (showDetailsForm) {
    return (
      <div className="sm:w-[42rem]">
        <h2 className="text-primary text-balance text-xl/6 font-semibold sm:text-lg/6">
          {t('form.creation.detailsHeadline', 'Create New Form')}
        </h2>
        <p className="text-secondary mt-2 text-sm">
          {t('form.creation.detailsDescription', 'Provide details for your new form')}
        </p>

        <Form.Simple
          className="mt-6 space-y-4 [&_[data-slot=submit]]:flex [&_[data-slot=submit]]:justify-end"
          form={rcForm}
          initialValues={{ mobileCategory: 'GENERAL' }}
          submitProps={{
            className: 'px-5 min-w-24',
            size: 'md',
            label: t('form.creation.createButton', 'Create Form'),
            loading
          }}
          onFinish={run}
        >
          <Form.Item
            name="name"
            label={t('form.creation.name.label', 'Form Name')}
            rules={[
              {
                required: true,
                message: t('form.creation.name.required', 'Please enter a form name')
              }
            ]}
          >
            <Input
              placeholder={t('form.creation.name.placeholder', 'e.g., Customer Feedback Survey')}
              autoComplete="off"
              maxLength={100}
            />
          </Form.Item>

          <Form.Item
            name="description"
            label={t('form.creation.description.label', 'Description')}
            description={t(
              'form.creation.description.help',
              'Optional description to help team members understand the form purpose'
            )}
          >
            <Input.TextArea
              placeholder={t('form.creation.description.placeholder', 'What is this form for?')}
              autoComplete="off"
              rows={3}
              maxLength={500}
            />
          </Form.Item>

          <Form.Item
            name="mobileCategory"
            label={t('form.creation.category.label', 'Category')}
            description={t(
              'form.creation.category.help',
              'Categorize your form for better organization'
            )}
            rules={[
              {
                required: true,
                message: t('form.creation.category.required', 'Please select a category')
              }
            ]}
          >
            <Select
              options={categoryOptions}
              placeholder={t('form.creation.category.placeholder', 'Select a category')}
            />
          </Form.Item>
        </Form.Simple>
      </div>
    )
  } else if (activeName === 'template') {
    return <TemplatesModel onBack={handleBack} />
  } else if (activeName === 'ai') {
    return <CreateWithAIModel onBack={handleBack} />
  } else {
    return (
      <>
        <h2 className="text-primary text-balance text-xl/6 font-semibold sm:text-lg/6">
          {t('form.creation.headline')}
        </h2>
        <div className="mt-6 grid grid-cols-1 gap-4 sm:w-[42rem] sm:grid-cols-3">
          {FORM_TYPES.map(row => (
            <Button.Link
              key={row.id}
              className="border-input flex h-auto border py-8 sm:aspect-square sm:h-auto sm:py-0 [&_[data-slot=button]]:h-full [&_[data-slot=button]]:flex-col"
              loading={row.id === 'scratch' && loading}
              disabled={loading}
              onClick={() => handleClick(row.id)}
            >
              <row.icon className="non-scaling-stroke h-9 w-9" />
              <div className="mt-2 text-sm/6 font-semibold">{t(row.headline)}</div>
              <div className="text-secondary mt-1 text-xs">{t(row.subHeadline)}</div>
            </Button.Link>
          ))}
        </div>
      </>
    )
  }
}

export default function CreateFormModal() {
  const { isOpen, onOpenChange } = useModal('CreateFormModal')

  return (
    <Modal
      open={isOpen}
      contentProps={{
        id: 'create-form-modal',
        className: 'sm:max-w-full sm:max-h-[90vh] w-auto'
      }}
      onOpenChange={onOpenChange}
    >
      <CreateFormComponent />
    </Modal>
  )
}
