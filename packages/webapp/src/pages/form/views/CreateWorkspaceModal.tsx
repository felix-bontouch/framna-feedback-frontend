import { observer } from 'mobx-react-lite'
import type { FC } from 'react'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'

import { WorkspaceModel } from '@/models'
import { WorkspaceService } from '@/services'
import { useRouter } from '@/utils'

import { PhotoPickerField } from '@/components'
import { Button, Form, Input, Modal } from '@/components'
import { useStore } from '@/store'

const CreateWorkspaceModal: FC<IModalProps> = observer(({ visible, onClose }) => {
  const { t } = useTranslation()
  const router = useRouter()
  const workspaceStore = useStore('workspaceStore')

  const [maskClosable, setMaskClosable] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  async function handleFinish(values: WorkspaceModel) {
    if (loading) {
      return
    }

    setLoading(true)

    try {
      const result = await WorkspaceService.create(values.name, values.avatar)

      const workspaces = await WorkspaceService.workspaces()
      workspaceStore.setWorkspaces(workspaces)

      onClose?.()

      router.replace(`/workspace/${result}`)
    } catch (err: any) {
      setLoading(false)
      setError(err)
    }
  }

  function handleVisibilityChange(newVal: boolean) {
    setMaskClosable(!newVal)
  }

  return (
    <Modal visible={visible} maskClosable={maskClosable} onClose={onClose} showCloseIcon>
      <div className="space-y-6">
        <div>
          <h1 className="text-lg font-medium leading-6 text-slate-900">
            {t('workspace.createWorkspace.newWorkspace')}
          </h1>
          <p className="mr-8 mt-1 text-base text-slate-500">
            {t('workspace.createWorkspace.text')}
          </p>
        </div>

        <Form onFinish={handleFinish}>
          <Form.Item
            name="name"
            label={t('workspace.createWorkspace.name')}
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="avatar"
            label={
              <>
                {t('workspace.createWorkspace.logo')}{' '}
                <span className="text-slate-500">({t('workspace.createWorkspace.optional')})</span>
              </>
            }
          >
            <PhotoPickerField onVisibilityChange={handleVisibilityChange} />
          </Form.Item>

          <Button className="w-full md:w-auto" type="primary" htmlType="submit" loading={loading}>
            {t('workspace.createWorkspace.create')}
          </Button>

          {error && <div className="form-item-error">{error.message}</div>}
        </Form>
      </div>
    </Modal>
  )
})

export default CreateWorkspaceModal
