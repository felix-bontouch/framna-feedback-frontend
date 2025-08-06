import { FieldKindEnum, LogicCondition } from '@heyform-inc/shared-types-enums'
import { type FC, useCallback, useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'

import { helper } from '@heyform-inc/utils'

import { Input, Select } from '@/components'
import {
  DATE_CONDITIONS,
  DEFAULT_COMPARISONS,
  MULTIPLE_CHOICE_CONDITIONS,
  NUMBER_CONDITIONS,
  SINGLE_CHOICE_CONDITIONS,
  TEXT_CONDITIONS,
  TRUE_FALSE_CONDITIONS
} from '@/consts'
import { FormFieldType } from '@/types'

interface ConditionProps {
  field: FormFieldType
  value?: LogicCondition
  onChange?: (value: LogicCondition) => void
}

interface DefaultProps {
  value?: any
  onComparisonChange: (value: any) => void
  onExpectedChange?: (value: any) => void
}

const DefaultCondition: FC<DefaultProps> = ({ value, onComparisonChange }) => {
  return (
    <Select
      className="w-auto flex-1"
      options={DEFAULT_COMPARISONS}
      value={value?.comparison}
      multiLanguage
      onChange={onComparisonChange}
    />
  )
}

const TextCondition: FC<DefaultProps> = ({ value, onComparisonChange, onExpectedChange }) => {
  return (
    <>
      <Select
        className="w-auto flex-1"
        options={TEXT_CONDITIONS}
        value={value?.comparison}
        multiLanguage
        onChange={onComparisonChange}
      />
      <Input
        className="flex-1"
        value={(value as Any).expected}
        placeholder="Value"
        onChange={onExpectedChange}
      />
    </>
  )
}

const SingleChoiceCondition: FC<DefaultProps & { field: FormFieldType }> = ({
  value,
  field,
  onComparisonChange,
  onExpectedChange
}) => {
  const choices = (field.properties?.choices || []) as AnyMap[]

  return (
    <>
      <Select
        className="w-auto flex-1"
        options={SINGLE_CHOICE_CONDITIONS}
        value={value?.comparison}
        multiLanguage
        onChange={onComparisonChange}
      />
      <Select
        className="flex-1"
        options={choices}
        valueKey="id"
        labelKey="label"
        value={value?.expected}
        onChange={onExpectedChange}
      />
    </>
  )
}

const MultipleChoiceCondition: FC<DefaultProps & { field: FormFieldType }> = ({
  value,
  field,
  onComparisonChange,
  onExpectedChange
}) => {
  const choices = (field.properties?.choices || []) as AnyMap[]

  // Use multi-select only for "contains" and "does_not_contain" when field allows multiple
  // Fix: Ensure we're checking the comparison value correctly
  const useMultiSelect = Boolean(
    field.properties?.allowMultiple === true &&
      (value?.comparison === 'contains' || value?.comparison === 'does_not_contain')
  )

  // Prepare the current value based on selection mode
  const currValue = useMemo(() => {
    // Debug logging to understand the issue
    console.log('MultipleChoiceCondition debug:', {
      comparison: value?.comparison,
      expected: value?.expected,
      expectedType: typeof value?.expected,
      expectedIsArray: helper.isArray(value?.expected),
      useMultiSelect,
      allowMultiple: field.properties?.allowMultiple,
      choices: choices.map(c => ({ id: c.id, label: c.label }))
    })

    if (useMultiSelect) {
      // For multi-select, ensure value is an array
      if (!value?.expected) return []
      return helper.isArray(value.expected) ? value.expected : [value.expected]
    } else {
      // For single-select, ensure value is a single value (not an array)
      if (!value?.expected) return undefined

      // If value.expected is an array but we're in single-select mode
      if (helper.isArray(value.expected)) {
        console.warn('Single-select received array value:', value.expected)
        // Return the first item or undefined
        return value.expected.length > 0 ? value.expected[0] : undefined
      }

      // Check if value.expected is the choices array itself
      if (value.expected === choices) {
        console.error('value.expected is the choices array itself!')
        return undefined
      }

      // Return the value as-is if it's already a single value
      return value.expected
    }
  }, [useMultiSelect, value?.expected, choices])

  // Handle comparison change
  const handleComparisonChange = useCallback(
    (newComparison: any) => {
      onComparisonChange(newComparison)

      // Clear value when switching between single/multi select modes
      const willUseMultiSelect =
        field.properties?.allowMultiple &&
        (newComparison === 'contains' || newComparison === 'does_not_contain')

      if (willUseMultiSelect !== useMultiSelect && onExpectedChange) {
        // Clear the value when switching modes to avoid confusion
        onExpectedChange(willUseMultiSelect ? [] : undefined)
      }
    },
    [field.properties?.allowMultiple, useMultiSelect, onComparisonChange, onExpectedChange]
  )

  return (
    <>
      <Select
        className="w-auto flex-1"
        options={MULTIPLE_CHOICE_CONDITIONS}
        value={value?.comparison}
        multiLanguage
        onChange={handleComparisonChange}
      />
      {useMultiSelect ? (
        <Select.Multi
          className="flex-1"
          options={choices}
          valueKey="id"
          labelKey="label"
          value={currValue}
          onChange={onExpectedChange}
        />
      ) : (
        <Select
          className="flex-1"
          options={choices}
          valueKey="id"
          labelKey="label"
          value={currValue}
          onChange={onExpectedChange}
        />
      )}
    </>
  )
}

const BoolCondition: FC<DefaultProps> = ({ value, onComparisonChange, onExpectedChange }) => {
  return (
    <>
      <Select
        className="w-auto flex-1"
        options={SINGLE_CHOICE_CONDITIONS}
        value={value?.comparison}
        multiLanguage
        onChange={onComparisonChange}
      />
      <Select
        className="flex-1"
        type="boolean"
        options={TRUE_FALSE_CONDITIONS}
        value={value?.expected}
        multiLanguage
        onChange={onExpectedChange}
      />
    </>
  )
}

const DateCondition: FC<DefaultProps> = ({ value, onComparisonChange, onExpectedChange }) => {
  return (
    <>
      <Select
        className="w-auto flex-1"
        options={DATE_CONDITIONS}
        value={value?.comparison}
        multiLanguage
        onChange={onComparisonChange}
      />
      <Input
        className="flex-1"
        type="number"
        value={(value as Any).expected}
        placeholder="Value"
        onChange={onExpectedChange}
      />
    </>
  )
}

const NumberCondition: FC<DefaultProps> = ({ value, onComparisonChange, onExpectedChange }) => {
  return (
    <>
      <Select
        className="w-auto flex-1"
        options={NUMBER_CONDITIONS}
        value={value?.comparison}
        multiLanguage
        onChange={onComparisonChange}
      />
      <Input
        className="flex-1"
        type="number"
        value={(value as Any).expected}
        placeholder="Value"
        onChange={onExpectedChange}
      />
    </>
  )
}

export default function Condition({ field, value: rawValue, onChange }: ConditionProps) {
  const { t } = useTranslation()
  const [value, setValue] = useState<LogicCondition>(rawValue!)

  useEffect(() => {
    if (rawValue) {
      setValue(rawValue)
    }
  }, [rawValue])

  const handleChange = useCallback(
    (newValue: any) => {
      setValue(newValue)
      onChange?.(newValue)
    },
    [onChange]
  )

  const handleComparisonChange = useCallback(
    (comparison: any) => {
      handleChange({ ...value, comparison })
    },
    [handleChange, value]
  )

  const handleExpectedChange = useCallback(
    (expected: any) => {
      handleChange({ ...value, expected })
    },
    [handleChange, value]
  )

  const Element = useMemo(() => {
    switch (field.kind) {
      case FieldKindEnum.SHORT_TEXT:
      case FieldKindEnum.LONG_TEXT:
      case FieldKindEnum.EMAIL:
      case FieldKindEnum.PHONE_NUMBER:
      case FieldKindEnum.URL:
      case FieldKindEnum.FULL_NAME:
      case FieldKindEnum.ADDRESS:
      case FieldKindEnum.COUNTRY:
        return (
          <TextCondition
            value={value}
            onComparisonChange={handleComparisonChange}
            onExpectedChange={handleExpectedChange}
          />
        )

      case FieldKindEnum.YES_NO:
        return (
          <SingleChoiceCondition
            field={field}
            value={value}
            onComparisonChange={handleComparisonChange}
            onExpectedChange={handleExpectedChange}
          />
        )

      case FieldKindEnum.LEGAL_TERMS:
        return (
          <BoolCondition
            value={value}
            onComparisonChange={handleComparisonChange}
            onExpectedChange={handleExpectedChange}
          />
        )

      case FieldKindEnum.MULTIPLE_CHOICE:
      case FieldKindEnum.PICTURE_CHOICE:
        return (
          <MultipleChoiceCondition
            field={field}
            value={value}
            onComparisonChange={handleComparisonChange}
            onExpectedChange={handleExpectedChange}
          />
        )

      case FieldKindEnum.DATE:
        return (
          <DateCondition
            value={value}
            onComparisonChange={handleComparisonChange}
            onExpectedChange={handleExpectedChange}
          />
        )

      case FieldKindEnum.NUMBER:
      case FieldKindEnum.RATING:
      case FieldKindEnum.OPINION_SCALE:
        return (
          <NumberCondition
            value={value}
            onComparisonChange={handleComparisonChange}
            onExpectedChange={handleExpectedChange}
          />
        )

      default:
        return <DefaultCondition value={value} onComparisonChange={handleComparisonChange} />
    }
  }, [field, handleComparisonChange, handleExpectedChange, value])

  return (
    <div className="rule-condition">
      <div className="text-sm leading-10">{t('form.builder.logic.rule.when')}</div>
      {Element}
    </div>
  )
}
