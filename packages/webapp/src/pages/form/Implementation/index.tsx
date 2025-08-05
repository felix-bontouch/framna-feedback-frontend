import { IconExclamationCircle } from '@tabler/icons-react'
import { useMemo } from 'react'

import { useParam } from '@/utils'

import { Button } from '@/components'
import { useFormStore, useWorkspaceStore } from '@/store'

import ApiReference from './ApiReference'

export default function FormImplementation() {
  const { formId } = useParam()
  const { sharingURLPrefix } = useWorkspaceStore()
  const { form } = useFormStore()

  const shareLink = useMemo(() => sharingURLPrefix + '/form/' + formId, [formId, sharingURLPrefix])

  return (
    <div className="mt-10 space-y-10">
      {form?.canPublish && (
        <div className="border-accent-light flex items-center justify-center gap-x-2 rounded-lg border bg-red-50 py-2">
          <IconExclamationCircle className="h-5 w-5 text-red-700" />
          <span className="text-sm/6 font-medium text-red-700">
            This form is not published yet. Publish it to make it available via API.
          </span>
        </div>
      )}

      <section id="link">
        <h2 className="text-base/6 font-semibold">Form Link</h2>
        <div className="mt-4">
          <div className="flex flex-col gap-2 text-sm/6 sm:flex-row sm:items-center">
            <div className="border-input flex items-center gap-x-4 rounded-lg border">
              <div className="h-10 flex-1 truncate pl-4 leading-10">{shareLink}</div>
              <Button.Copy className="rounded-l-none" text={shareLink} />
            </div>
          </div>
          <p className="text-secondary mt-2 text-sm">
            Use this link to share your form. Mobile apps can open this link directly or use the API
            endpoints below.
          </p>
        </div>
      </section>

      <ApiReference formId={formId} shareLink={shareLink} />
    </div>
  )
}
