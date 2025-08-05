import { useBoolean } from 'ahooks'
import { Trans, useTranslation } from 'react-i18next'

import { ProjectService } from '@/services'
import { useParam, useRouter } from '@/utils'

import { Form, Input, Modal, useToast } from '@/components'
import { useModal, useWorkspaceStore } from '@/store'

export default function DeleteProjectModal() {
  const { t } = useTranslation()

  const toast = useToast()
  const router = useRouter()

  const { workspaceId } = useParam()
  const { deleteProject } = useWorkspaceStore()

  const { isOpen, payload, onOpenChange } = useModal('DeleteProjectModal')
  const [loading, { set }] = useBoolean(false)

  async function fetch(values: any) {
    if (values.code !== 'delete') {
      toast({
        title: t('project.delete.invalidCode'),
        message: t('project.delete.invalidCodeMessage')
      })
      return
    }

    await ProjectService.delete(payload.id, values.code)

    deleteProject(workspaceId, payload.id)
    onOpenChange(false)

    router.replace(`/workspace/${workspaceId}`)
  }

  return (
    <Modal.Simple
      open={isOpen}
      title={t('project.delete.headline')}
      description={
        <div className="text-secondary space-y-2.5 text-sm">
          <p>
            <Trans
              t={t}
              i18nKey="project.delete.tip1"
              values={{
                name: payload?.name
              }}
              components={{
                strong: <strong className="text-primary" />
              }}
            />
          </p>
          <p>{t('project.delete.tip2')}</p>
          <p>{t('project.delete.tip3')}</p>
        </div>
      }
      contentProps={{
        className: 'max-w-md'
      }}
      loading={loading}
      onOpenChange={onOpenChange}
    >
      <Form.Simple
        className="space-y-4"
        fetch={fetch}
        refreshDeps={[workspaceId, payload?.id]}
        submitProps={{
          className: 'px-5 w-full text-primary-light dark:text-primary bg-error hover:bg-error',
          size: 'md',
          label: t('project.delete.confirm')
        }}
        submitOnChangedOnly
        onLoadingChange={set}
      >
        <Form.Item
          name="code"
          label={t('project.delete.code.label')}
          rules={[
            {
              required: true,
              message: t('project.delete.code.required')
            },
            {
              pattern: /^delete$/,
              message: t('project.delete.code.invalid')
            }
          ]}
        >
          <Input autoComplete="off" placeholder={t('project.delete.code.placeholder')} />
        </Form.Item>
      </Form.Simple>
    </Modal.Simple>
  )
}
