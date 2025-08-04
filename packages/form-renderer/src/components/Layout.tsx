import type { Layout as FormLayout } from '@heyform-inc/shared-types-enums'
import type { FC } from 'react'
import { memo } from 'react'

import { isURL } from '../utils'
import { deepEqual, helper } from '@heyform-inc/utils'

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

const LayoutComponent: FC<FormLayout> = props => {
  // Layout images are disabled - no images allowed in forms
  return null
}

export const Layout = memo(LayoutComponent, deepEqual)
