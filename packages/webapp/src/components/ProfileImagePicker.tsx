import * as Dialog from '@radix-ui/react-dialog'
import { VisuallyHidden } from '@radix-ui/react-visually-hidden'
import { IconX } from '@tabler/icons-react'
import { FC, useState } from 'react'
import { useTranslation } from 'react-i18next'

import { Avatar } from './Avatar'
import { Button } from './Button'
import { Uploader } from './Uploader'

interface ProfileImagePickerProps {
  value?: string
  fallback?: string
  onUpload?: (url?: string) => void
}

export const ProfileImagePicker: FC<ProfileImagePickerProps> = ({ value, fallback, onUpload }) => {
  const { t } = useTranslation()
  const [isOpen, setOpen] = useState(false)

  const handleChange = (url?: string) => {
    setOpen(false)
    onUpload?.(url)
  }

  return (
    <>
      <div className="flex items-center gap-x-3">
        <Avatar
          src={value}
          fallback={fallback}
          resize={{ width: 200, height: 200 }}
          className="h-16 w-16"
        />
        <div className="space-y-1">
          <Button.Ghost size="sm" onClick={() => setOpen(true)}>
            {value ? t('components.change') : t('components.uploader.uploadImage')}
          </Button.Ghost>
          {value && (
            <Button.Link
              size="sm"
              className="text-error hover:text-error/80"
              onClick={() => onUpload?.(undefined)}
            >
              {t('components.remove')}
            </Button.Link>
          )}
        </div>
      </div>

      <Dialog.Root open={isOpen} onOpenChange={setOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 fixed inset-0 z-10 bg-black/60" />
          <Dialog.Content className="border-accent-light bg-foreground data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:slide-out-to-bottom-0 data-[state=open]:slide-in-from-bottom-[80%] data-[state=closed]:sm:zoom-out-95 data-[state=open]:sm:zoom-in-95 data-[state=closed]:sm:slide-out-to-left-1/2 data-[state=closed]:sm:slide-out-to-top-[48%] data-[state=open]:sm:slide-in-from-left-1/2 data-[state=open]:sm:slide-in-from-top-[48%] fixed bottom-0 left-0 right-0 z-10 w-full max-w-lg rounded-lg border shadow-lg duration-200 sm:bottom-auto sm:left-[50%] sm:right-auto sm:top-[50%] sm:max-w-md sm:translate-x-[-50%] sm:translate-y-[-50%]">
            <Dialog.Title>
              <VisuallyHidden>{t('components.profileImagePicker.title')}</VisuallyHidden>
            </Dialog.Title>
            <Dialog.Description>
              <VisuallyHidden>{t('components.profileImagePicker.description')}</VisuallyHidden>
            </Dialog.Description>

            <div className="relative p-6">
              <Dialog.Close asChild>
                <Button.Link
                  className="text-secondary hover:text-primary absolute right-2 top-2"
                  size="sm"
                  iconOnly
                >
                  <span className="sr-only">{t('components.close')}</span>
                  <IconX className="h-5 w-5" />
                </Button.Link>
              </Dialog.Close>

              <h2 className="mb-4 text-lg font-semibold">
                {t('components.profileImagePicker.title')}
              </h2>

              <div className="h-64">
                <Uploader
                  accept={['image/jpeg', 'image/png', 'image/webp', 'image/gif']}
                  maxSize="5MB"
                  title={t('components.profileImagePicker.uploadTitle')}
                  description={t('components.profileImagePicker.uploadDescription')}
                  onChange={handleChange}
                />
              </div>
            </div>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </>
  )
}
