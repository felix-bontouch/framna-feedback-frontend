import { useBoolean } from 'ahooks'
import { Trans, useTranslation } from 'react-i18next'

import { WorkspaceService } from '@/services'
import { useRouter } from '@/utils'

import { Form, Input, Modal, useToast } from '@/components'
import { useModal, useWorkspaceStore } from '@/store'

export default function WorkspaceDeletionModal() {
  const { t } = useTranslation()

  const toast = useToast()
  const router = useRouter()

  const { deleteWorkspace } = useWorkspaceStore()

  const { isOpen, payload, onOpenChange } = useModal('WorkspaceDeletionModal')
  const [loading, { set }] = useBoolean(false)

  async function fetch(values: any) {
    if (values.code !== 'delete') {
      toast({
        title: t('workspace.delete.invalidCode'),
        message: t('workspace.delete.invalidCodeMessage')
      })
      return
    }

    await WorkspaceService.dissolve(payload.id, values.code)

    deleteWorkspace(payload.id)
    router.replace('/')
  }

  return (
    <Modal.Simple
      open={isOpen}
      title={t('settings.deletion.headline')}
      description={
        <div className="text-secondary space-y-2.5 text-sm">
          <p>
            <Trans
              t={t}
              i18nKey="settings.deletion.tip1"
              values={{
                name: payload?.name
              }}
              components={{
                strong: <strong className="text-primary" />
              }}
            />
          </p>
          <p>{t('settings.deletion.tip2')}</p>
          <p>{t('settings.deletion.tip3')}</p>
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
        refreshDeps={[payload?.id]}
        submitProps={{
          className: 'px-5 w-full bg-error text-primary-light dark:text-primary hover:bg-error',
          size: 'md',
          label: t('settings.deletion.button')
        }}
        submitOnChangedOnly
        onLoadingChange={set}
      >
        <Form.Item
          name="code"
          label={t('workspace.delete.code.label')}
          rules={[
            {
              required: true,
              message: t('workspace.delete.code.required')
            },
            {
              pattern: /^delete$/,
              message: t('workspace.delete.code.invalid')
            }
          ]}
        >
          <Input autoComplete="off" placeholder={t('workspace.delete.code.placeholder')} />
        </Form.Item>
      </Form.Simple>
    </Modal.Simple>
  )
}
