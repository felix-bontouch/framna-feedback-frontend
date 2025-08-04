import { expect, test } from 'vitest'

import { helper, uuidv4 } from '../src'

test('uuidv4', () => {
  expect(helper.isUUID(uuidv4())).toBe(true)
})
