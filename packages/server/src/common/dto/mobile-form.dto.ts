import { Type } from 'class-transformer'
import {
  IsArray,
  IsBoolean,
  IsNotEmpty,
  IsNumber,
  IsObject,
  IsOptional,
  IsString,
  ValidateNested
} from 'class-validator'

// Request DTOs
export class MobileFieldsQueryDto {
  @IsOptional()
  @IsString()
  fieldIds?: string
}

export class ClientInfoDto {
  @IsOptional()
  @IsString()
  ip?: string

  @IsOptional()
  @IsString()
  userAgent?: string

  @IsString()
  @IsNotEmpty()
  os: string

  @IsString()
  @IsNotEmpty()
  osVersion: string

  @IsString()
  @IsNotEmpty()
  appVersion: string

  @IsString()
  @IsNotEmpty()
  device: string

  @IsOptional()
  @IsString()
  deviceId?: string

  @IsOptional()
  @IsString()
  locale?: string
}

export class HiddenFieldDto {
  @IsString()
  @IsNotEmpty()
  id: string

  value: any
}

export class MobileSubmissionRequestDto {
  @IsObject()
  @IsNotEmpty()
  answers: Record<string, any>

  @IsNumber()
  startedAt: number

  @ValidateNested()
  @Type(() => ClientInfoDto)
  clientInfo: ClientInfoDto

  @IsOptional()
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => HiddenFieldDto)
  hiddenFields?: HiddenFieldDto[]

  @IsOptional()
  @IsString()
  password?: string

  @IsOptional()
  @IsString()
  captchaToken?: string

  @IsOptional()
  @IsBoolean()
  isPartial?: boolean

  @IsOptional()
  @IsString()
  category?: 'NPS' | 'FEATURE' | 'USER_FLOW' | 'PERFORMANCE' | 'GENERAL' | 'ONBOARDING' | 'RATING'
}

// Response DTOs
export class MobileFormFieldDto {
  id: string
  kind: string
  title?: string
  description?: string
  validations?: any
  width?: number
  hide?: boolean
  frozen?: boolean
  properties?: any
}

export class MobileFormSettingsDto {
  active: boolean
  captchaKind?: string
  requirePassword?: boolean
  redirectOnCompletion?: boolean
  redirectUrl?: string
  filterSpam?: boolean
  allowArchive?: boolean
  locale?: string
  languages?: string[]
  enableQuotaLimit?: boolean
  quotaLimit?: number
  enableIpLimit?: boolean
  ipLimitCount?: number
}

export class MobileFormResponseDto {
  id: string
  teamId: string
  projectId: string
  name: string
  description?: string
  interactiveMode: number
  kind: number
  settings: MobileFormSettingsDto
  fields: MobileFormFieldDto[]
  hiddenFields: any[]
  logics: any[]
  variables: any[]
  translations: Record<string, any>
  fieldsUpdatedAt: number
  suspended: boolean
  version: number
}

export class MobileSubmissionResponseDto {
  success: boolean
  submissionId: string
  timestamp: number
  redirectUrl?: string
  message: string
}

export class MobileFormShareInfoDto {
  shareUrl: string
  isPublished: boolean
  isActive: boolean
  metadata: {
    title: string
    description: string
    ogImageUrl?: string
    questionCount: number
    estimatedTime: number
  }
  accessControl: {
    requiresPassword: boolean
    hasIpLimit: boolean
    hasTimeLimit: boolean
    expiresAt?: string
  }
}

export class UpdateFormSettingsDto {
  @IsOptional()
  @IsString()
  metaTitle?: string

  @IsOptional()
  @IsString()
  metaDescription?: string

  @IsOptional()
  @IsString()
  metaOGImageUrl?: string
}
