import { FieldKindEnum, FieldLayoutAlignEnum } from '@heyform-inc/shared-types-enums'
import { IconCalendar, IconEyeOff, IconVariable } from '@tabler/icons-react'

import IconAddress from '@/assets/address.svg?react'
import IconCountry from '@/assets/country.svg?react'
import IconDateRange from '@/assets/date-range.svg?react'
import IconDateTime from '@/assets/date-time.svg?react'
import IconEmail from '@/assets/email.svg?react'
import IconFullPage from '@/assets/embed-fullpage.svg?react'
import IconModal from '@/assets/embed-modal.svg?react'
import IconPopup from '@/assets/embed-popup.svg?react'
import IconStandard from '@/assets/embed-standard.svg?react'
import IconFileUpload from '@/assets/file-upload.svg?react'
import IconFullName from '@/assets/full-name.svg?react'
import IconInputTable from '@/assets/input-table.svg?react'
import IconLayoutCover from '@/assets/layout-cover.svg?react'
import IconLayoutFloatLeft from '@/assets/layout-float-left.svg?react'
import IconLayoutFloatRight from '@/assets/layout-float-right.svg?react'
import IconLayoutInline from '@/assets/layout-inline.svg?react'
import IconLayoutSplitLeft from '@/assets/layout-split-left.svg?react'
import IconLayoutSplitRight from '@/assets/layout-split-right.svg?react'
import IconLegalTerms from '@/assets/legal-terms.svg?react'
import IconLongText from '@/assets/long-text.svg?react'
import IconMultipleIcon from '@/assets/multiple-choice.svg?react'
import IconNumber from '@/assets/number.svg?react'
import IconOpinionScale from '@/assets/opinion-scale.svg?react'
import IconPhoneNumber from '@/assets/phone-number.svg?react'
import IconQuestionGroup from '@/assets/question-group.svg?react'
import IconRating from '@/assets/rating.svg?react'
import IconShortText from '@/assets/short-text.svg?react'
import IconSignature from '@/assets/signature.svg?react'
import IconStatement from '@/assets/statement.svg?react'
import IconThankYou from '@/assets/thank-you.svg?react'
import IconVariableNumber from '@/assets/variable-number.svg?react'
import IconVariableString from '@/assets/variable-string.svg?react'
import IconWebsite from '@/assets/website.svg?react'
import IconWelcome from '@/assets/welcome.svg?react'
import IconYesNo from '@/assets/yes-no.svg?react'

export const FIELD_WELCOME_CONFIG = {
  kind: FieldKindEnum.WELCOME,
  icon: IconWelcome,
  label: 'form.builder.question.welcome',
  textColor: '#334155',
  backgroundColor: '#e5e7eb'
}

export const FIELD_THANK_YOU_CONFIG = {
  kind: FieldKindEnum.THANK_YOU,
  icon: IconThankYou,
  label: 'form.builder.question.thankYou',
  textColor: '#334155',
  backgroundColor: '#e5e7eb'
}

export const STANDARD_FIELD_CONFIGS = [
  {
    kind: FieldKindEnum.MULTIPLE_CHOICE,
    icon: IconMultipleIcon,
    label: 'form.builder.question.multipleChoice',
    textColor: '#b91c1c',
    backgroundColor: '#fee2e2'
  },
  {
    kind: FieldKindEnum.PHONE_NUMBER,
    icon: IconPhoneNumber,
    label: 'form.builder.question.phoneNumber',
    textColor: '#0369a1',
    backgroundColor: '#e0f2fe'
  },
  {
    kind: FieldKindEnum.SHORT_TEXT,
    icon: IconShortText,
    label: 'form.builder.question.shortText',
    textColor: '#15803d',
    backgroundColor: '#dcfce7'
  },
  {
    kind: FieldKindEnum.LONG_TEXT,
    icon: IconLongText,
    label: 'form.builder.question.longText',
    textColor: '#15803d',
    backgroundColor: '#dcfce7'
  },
  {
    kind: FieldKindEnum.GROUP,
    icon: IconQuestionGroup,
    label: 'form.builder.question.questionGroup',
    textColor: '#334155',
    backgroundColor: '#e5e7eb'
  },
  {
    kind: FieldKindEnum.STATEMENT,
    icon: IconStatement,
    label: 'form.builder.question.statement',
    textColor: '#334155',
    backgroundColor: '#e5e7eb'
  },
  {
    kind: FieldKindEnum.YES_NO,
    icon: IconYesNo,
    label: 'form.builder.question.yesNo',
    textColor: '#b91c1c',
    backgroundColor: '#fee2e2'
  },
  {
    kind: FieldKindEnum.EMAIL,
    icon: IconEmail,
    label: 'form.builder.question.email',
    textColor: '#0369a1',
    backgroundColor: '#e0f2fe'
  },
  {
    kind: FieldKindEnum.FULL_NAME,
    icon: IconFullName,
    label: 'form.builder.question.fullName',
    textColor: '#0369a1',
    backgroundColor: '#e0f2fe'
  },
  {
    kind: FieldKindEnum.RATING,
    icon: IconRating,
    label: 'form.builder.question.rating',
    textColor: '#a21caf',
    backgroundColor: '#fae8ff'
  },
  {
    kind: FieldKindEnum.OPINION_SCALE,
    icon: IconOpinionScale,
    label: 'form.builder.question.opinionScale',
    textColor: '#a21caf',
    backgroundColor: '#fae8ff'
  },
  {
    kind: FieldKindEnum.DATE,
    icon: IconDateTime,
    label: 'form.builder.question.dateTime',
    textColor: '#059669',
    backgroundColor: '#a7f3d0'
  },
  {
    kind: FieldKindEnum.DATE_RANGE,
    icon: IconDateRange,
    label: 'form.builder.question.dateRange',
    textColor: '#059669',
    backgroundColor: '#a7f3d0'
  },
  {
    kind: FieldKindEnum.NUMBER,
    icon: IconNumber,
    label: 'form.builder.question.number',
    textColor: '#0f766e',
    backgroundColor: '#ccfbf1'
  },
  {
    kind: FieldKindEnum.FILE_UPLOAD,
    icon: IconFileUpload,
    label: 'form.builder.question.fileUpload',
    textColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  },
  {
    kind: FieldKindEnum.ADDRESS,
    icon: IconAddress,
    label: 'form.builder.question.address',
    textColor: '#0369a1',
    backgroundColor: '#e0f2fe'
  },
  {
    kind: FieldKindEnum.COUNTRY,
    icon: IconCountry,
    label: 'form.builder.question.country',
    textColor: '#0369a1',
    backgroundColor: '#e0f2fe'
  },
  {
    kind: FieldKindEnum.LEGAL_TERMS,
    icon: IconLegalTerms,
    label: 'form.builder.question.legalTerms',
    textColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  },
  {
    kind: FieldKindEnum.SIGNATURE,
    icon: IconSignature,
    label: 'form.builder.question.signature',
    textColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  },
  {
    kind: FieldKindEnum.URL,
    icon: IconWebsite,
    label: 'form.builder.question.website',
    textColor: '#0369a1',
    backgroundColor: '#e0f2fe'
  },
  {
    kind: FieldKindEnum.INPUT_TABLE,
    icon: IconInputTable,
    label: 'form.builder.question.inputTable',
    textColor: '#c2410c',
    backgroundColor: '#ffedd5'
  }
]

export const ALL_FIELD_CONFIGS = [
  FIELD_WELCOME_CONFIG,
  FIELD_THANK_YOU_CONFIG,
  ...STANDARD_FIELD_CONFIGS
]

export const CUSTOM_FIELDS_CONFIGS = [
  {
    kind: FieldKindEnum.SUBMIT_DATE,
    icon: IconCalendar,
    label: 'form.builder.question.submitDate',
    textColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  },
  {
    kind: FieldKindEnum.HIDDEN_FIELDS,
    icon: IconEyeOff,
    label: 'form.builder.question.hiddenFields',
    textColor: '#334155',
    backgroundColor: '#e5e7eb'
  },
  {
    kind: FieldKindEnum.VARIABLE,
    icon: IconVariable,
    label: 'form.builder.question.variable',
    textColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  }
]

export const BLOCK_GROUPS = [
  [
    {
      name: 'form.builder.question.recommended',
      list: [
        FieldKindEnum.SHORT_TEXT,
        FieldKindEnum.MULTIPLE_CHOICE,
        FieldKindEnum.STATEMENT,
        FieldKindEnum.OPINION_SCALE,
        FieldKindEnum.EMAIL,
        FieldKindEnum.FULL_NAME
      ]
    }
  ],
  [
    {
      name: 'form.builder.question.contactInfo',
      list: [
        FieldKindEnum.PHONE_NUMBER,
        FieldKindEnum.EMAIL,
        FieldKindEnum.FULL_NAME,
        FieldKindEnum.ADDRESS,
        FieldKindEnum.COUNTRY,
        FieldKindEnum.URL
      ]
    },
    {
      name: 'form.builder.question.text',
      list: [FieldKindEnum.SHORT_TEXT, FieldKindEnum.LONG_TEXT]
    },

    {
      name: 'form.builder.question.fileUpload',
      list: [FieldKindEnum.FILE_UPLOAD]
    }
  ],
  [
    {
      name: 'form.builder.question.choices',
      list: [FieldKindEnum.MULTIPLE_CHOICE, FieldKindEnum.YES_NO]
    },
    {
      name: 'form.builder.question.rating',
      list: [FieldKindEnum.RATING, FieldKindEnum.OPINION_SCALE]
    },
    {
      name: 'form.builder.question.date',
      list: [FieldKindEnum.DATE, FieldKindEnum.DATE_RANGE]
    }
  ],
  [
    {
      name: 'form.builder.question.formStructure',
      list: [
        FieldKindEnum.GROUP,
        FieldKindEnum.STATEMENT,
        FieldKindEnum.WELCOME,
        FieldKindEnum.THANK_YOU
      ]
    },
    {
      name: 'form.builder.question.number',
      list: [FieldKindEnum.NUMBER]
    },
    {
      name: 'form.builder.question.data',
      list: [FieldKindEnum.INPUT_TABLE]
    },
    {
      name: 'form.builder.question.legalConsent',
      list: [FieldKindEnum.LEGAL_TERMS, FieldKindEnum.SIGNATURE]
    }
  ]
]

export const LAYOUT_OPTIONS = [
  {
    value: FieldLayoutAlignEnum.INLINE,
    icon: IconLayoutInline
  },
  {
    value: FieldLayoutAlignEnum.FLOAT_LEFT,
    icon: IconLayoutFloatLeft
  },
  {
    value: FieldLayoutAlignEnum.FLOAT_RIGHT,
    icon: IconLayoutFloatRight
  },
  {
    value: FieldLayoutAlignEnum.SPLIT_LEFT,
    icon: IconLayoutSplitLeft
  },
  {
    value: FieldLayoutAlignEnum.SPLIT_RIGHT,
    icon: IconLayoutSplitRight
  },
  {
    value: FieldLayoutAlignEnum.COVER,
    icon: IconLayoutCover
  }
]

export const DATE_FORMAT_OPTIONS = [
  {
    label: 'MM/DD/YYYY',
    value: 'MM/DD/YYYY'
  },
  {
    label: 'DD/MM/YYYY',
    value: 'DD/MM/YYYY'
  },
  {
    label: 'YYYY/MM/DD',
    value: 'YYYY/MM/DD'
  },
  {
    label: 'MM-DD-YYYY',
    value: 'MM-DD-YYYY'
  },
  {
    label: 'DD-MM-YYYY',
    value: 'DD-MM-YYYY'
  },
  {
    label: 'YYYY-MM-DD',
    value: 'YYYY-MM-DD'
  },
  {
    label: 'MM.DD.YYYY',
    value: 'MM.DD.YYYY'
  },
  {
    label: 'DD.MM.YYYY',
    value: 'DD.MM.YYYY'
  },
  {
    label: 'YYYY.MM.DD',
    value: 'YYYY.MM.DD'
  }
]

export const DATE_FORMAT_MAPS: AnyMap = {
  'MM/DD/YYYY': ['MM', 'DD', 'YYYY', '/'],
  'DD/MM/YYYY': ['DD', 'MM', 'YYYY', '/'],
  'YYYY/MM/DD': ['YYYY', 'MM', 'DD', '/'],
  'MM-DD-YYYY': ['MM', 'DD', 'YYYY', '-'],
  'DD-MM-YYYY': ['DD', 'MM', 'YYYY', '-'],
  'YYYY-MM-DD': ['YYYY', 'MM', 'DD', '-'],
  'MM.DD.YYYY': ['MM', 'DD', 'YYYY', '.'],
  'DD.MM.YYYY': ['DD', 'MM', 'YYYY', '.'],
  'YYYY.MM.DD': ['YYYY', 'MM', 'DD', '.'],
  'HH:mm': ['HH', 'mm', ':']
}

export const DATE_FORMAT_NAMES: AnyMap = {
  YYYY: {
    id: 'year',
    label: 'Year'
  },
  MM: {
    id: 'month',
    label: 'Month'
  },
  DD: {
    id: 'day',
    label: 'Day'
  },
  HH: {
    id: 'hour',
    label: 'Hour'
  },
  mm: {
    id: 'minute',
    label: 'Minute'
  }
}

export const FORM_EMBED_OPTIONS = [
  {
    value: 'standard',
    label: 'form.share.embed.standard',
    icon: IconStandard
  },
  {
    value: 'modal',
    label: 'form.share.embed.modal',
    icon: IconModal
  },
  {
    value: 'popup',
    label: 'form.share.embed.popup',
    icon: IconPopup
  },
  {
    value: 'fullpage',
    label: 'form.share.embed.fullpage',
    icon: IconFullPage
  }
]

export const DEFAULT_EMBED_CONFIGS = {
  standard: {
    widthType: '%',
    width: 100,
    heightType: 'px',
    height: 500,
    autoResizeHeight: true
  },
  modal: {
    size: 'large',
    openTrigger: 'click',
    openDelay: 5,
    openScrollPercent: 30,
    triggerBackground: '#1d4ed8',
    triggerText: 'Open Form',
    hideAfterSubmit: false,
    autoClose: 5
  },
  popup: {
    position: 'bottom-right',
    width: 420,
    height: 540,
    openTrigger: 'click',
    openDelay: 5,
    openScrollPercent: 30,
    triggerBackground: '#1d4ed8',
    hideAfterSubmit: false,
    autoClose: 5
  },
  fullpage: {
    transparentBackground: false
  }
}

export const INTEGRATION_CATEGORIES = [
  { value: 'Reporting', label: 'form.integrations.reporting' },
  { value: 'Analytics', label: 'form.integrations.analytics' },
  { value: 'Marketing', label: 'form.integrations.marketing' },
  { value: 'Automation', label: 'form.integrations.automation' },
  { value: 'Customer Support', label: 'form.integrations.customerSupport' },
  { value: 'Productivity', label: 'form.integrations.productivity' },
  { value: 'IT & Engineering', label: 'form.integrations.itEngineering' },
  { value: 'File Management', label: 'form.integrations.fileManagement' }
]

export enum APP_STATUS_ENUM {
  PENDING = 0,
  ACTIVE = 1,
  REDIRECT_TO_EXTERNAL = 2
}

export enum INTEGRATION_STATUS_ENUM {
  PERMITTED = 0,
  ACTIVE = 1,
  DISABLED
}

export const TEMPLATE_CATEGORIES = [
  'Contact',
  'Registration',
  'Survey',
  'Quiz',
  'Poll',
  'Form',
  'Application',
  'Booking',
  'Order',
  'Payment',
  'Donation',
  'RSVP',
  'Feedback',
  'Other'
]

export const ACTIONS = [
  { value: 'navigate', label: 'form.builder.logic.action.navigate' },
  { value: 'calculate', label: 'form.builder.logic.action.calculate' }
]

export const OPERATORS = [
  { value: 'add', label: 'form.builder.logic.operator.add' },
  { value: 'subtract', label: 'form.builder.logic.operator.subtract' },
  { value: 'multiply', label: 'form.builder.logic.operator.multiply' },
  { value: 'divide', label: 'form.builder.logic.operator.divide' }
]

export const VARIABLE_KIND_CONFIGS = [
  {
    kind: 'number',
    icon: IconVariableNumber,
    color: '#FFF',
    backgroundColor: '#00C4CC'
  },
  {
    kind: 'string',
    icon: IconVariableString,
    color: '#FFF',
    backgroundColor: '#2D7FF9'
  }
]

export const VARIABLE_INPUT_TYPES = {
  string: 'text',
  number: 'number'
}

export const SINGLE_CHOICE_CONDITIONS = [
  {
    value: 'is',
    label: 'form.builder.logic.rule.is'
  },
  {
    value: 'is_not',
    label: 'form.builder.logic.rule.isNot'
  }
]

export const TRUE_FALSE_CONDITIONS = [
  {
    value: true,
    label: 'form.builder.logic.rule.true'
  },
  {
    value: false,
    label: 'form.builder.logic.rule.false'
  }
]

export const MULTIPLE_CHOICE_CONDITIONS = [
  ...SINGLE_CHOICE_CONDITIONS,
  {
    value: 'contains',
    label: 'form.builder.logic.rule.contains'
  },
  {
    value: 'does_not_contain',
    label: 'form.builder.logic.rule.doesNotContain'
  }
]

export const TEXT_CONDITIONS = [
  ...MULTIPLE_CHOICE_CONDITIONS,
  {
    value: 'starts_with',
    label: 'form.builder.logic.rule.startsWith'
  },
  {
    value: 'ends_with',
    label: 'form.builder.logic.rule.endsWith'
  }
]

export const DATE_CONDITIONS = [
  ...SINGLE_CHOICE_CONDITIONS,
  {
    value: 'is_before',
    label: 'form.builder.logic.rule.isBefore'
  },
  {
    value: 'is_after',
    label: 'form.builder.logic.rule.isAfter'
  }
]

export const NUMBER_CONDITIONS = [
  {
    value: 'equal',
    label: 'form.builder.logic.rule.equal'
  },
  {
    value: 'not_equal',
    label: 'form.builder.logic.rule.notEqual'
  },
  {
    value: 'greater_than',
    label: 'form.builder.logic.rule.greaterThan'
  },
  {
    value: 'greater_or_equal_than',
    label: 'form.builder.logic.rule.greaterOrEqualThan'
  },
  {
    value: 'less_or_equal_than',
    label: 'form.builder.logic.rule.lessOrEqualThan'
  }
]

export const DEFAULT_COMPARISONS = [
  {
    value: 'is_empty',
    label: 'form.builder.logic.rule.isEmpty'
  },
  {
    value: 'is_not_empty',
    label: 'form.builder.logic.rule.isNotEmpty'
  }
]
