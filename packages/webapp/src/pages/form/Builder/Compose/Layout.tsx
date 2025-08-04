import type { Layout as FormLayout } from '@heyform-inc/shared-types-enums'
import type { FC } from 'react'

import { cn } from '@/utils'
import { helper } from '@heyform-inc/utils'

interface LayoutProps extends ComponentProps {
  layout?: FormLayout
}

function filterStyle(brightness?: number) {
  if (!brightness) {
    return undefined
  }

  const value = 1 + brightness / 100

  if (value < 0) {
    return {
      filter: `brightness(${value})`
    }
  }

  return {
    filter: `contrast(${2 - value}) brightness(${value})`
  }
}

export const Layout: FC<LayoutProps> = ({ className, layout, ...restProps }) => {
  // Layout images are disabled - no images allowed in forms
  return null
}
