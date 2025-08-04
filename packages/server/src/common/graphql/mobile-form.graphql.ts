import {
  FieldKindEnum,
  FormField,
  HiddenField,
  Logic,
  Property,
  Validation,
  Variable
} from '@heyform-inc/shared-types-enums'

import { FormModel } from '@model'
import { Field, ObjectType } from '@nestjs/graphql'
import GraphQLJSON from 'graphql-type-json'

@ObjectType()
export class MobileFieldType {
  @Field()
  id: string

  @Field(type => GraphQLJSON, { nullable: true })
  title?: any[]

  @Field(type => GraphQLJSON, { nullable: true })
  description?: any[]

  @Field(type => String)
  kind: FieldKindEnum

  @Field(type => GraphQLJSON, { nullable: true })
  validations?: Validation

  @Field(type => GraphQLJSON, { nullable: true })
  properties?: Property

  @Field({ nullable: true })
  width?: number

  @Field({ nullable: true })
  hide?: boolean

  @Field({ nullable: true })
  frozen?: boolean
}

@ObjectType()
export class MobileFormSettingsType {
  @Field({ nullable: true })
  captchaKind?: number

  @Field({ nullable: true })
  active?: boolean

  @Field({ nullable: true })
  enableExpirationDate?: boolean

  @Field({ nullable: true })
  expirationTimeZone?: string

  @Field({ nullable: true })
  enabledAt?: number

  @Field({ nullable: true })
  closedAt?: number

  @Field({ nullable: true })
  enableTimeLimit?: boolean

  @Field({ nullable: true })
  timeLimit?: number

  @Field({ nullable: true })
  filterSpam?: boolean

  @Field({ nullable: true })
  allowArchive?: boolean

  @Field({ nullable: true })
  requirePassword?: boolean

  @Field({ nullable: true })
  redirectOnCompletion?: boolean

  @Field({ nullable: true })
  redirectUrl?: string

  @Field({ nullable: true })
  redirectDelay?: number

  @Field({ nullable: true })
  enableQuotaLimit?: boolean

  @Field({ nullable: true })
  quotaLimit?: number

  @Field({ nullable: true })
  enableIpLimit?: boolean

  @Field({ nullable: true })
  ipLimitCount?: number

  @Field({ nullable: true })
  ipLimitTime?: number

  @Field({ nullable: true })
  enableProgress?: boolean

  @Field({ nullable: true })
  enableQuestionList?: boolean

  @Field({ nullable: true })
  enableNavigationArrows?: boolean

  @Field({ nullable: true })
  locale?: string

  @Field(type => [String], { nullable: true, defaultValue: [] })
  languages?: string[]

  @Field({ nullable: true })
  enableClosedMessage?: boolean

  @Field({ nullable: true })
  closedFormTitle?: string

  @Field({ nullable: true })
  closedFormDescription?: string

  @Field({ nullable: true })
  enableEmailNotification?: boolean
}

@ObjectType()
export class MobileFormType {
  @Field()
  id: string

  @Field()
  teamId: string

  @Field()
  projectId: string

  @Field()
  memberId: string

  @Field()
  name: string

  @Field({ nullable: true })
  description?: string

  @Field()
  interactiveMode: number

  @Field()
  kind: number

  @Field(type => MobileFormSettingsType, { nullable: true })
  settings?: MobileFormSettingsType

  @Field(type => [MobileFieldType], { nullable: true })
  fields: FormField[]

  @Field(type => GraphQLJSON, { nullable: true })
  translations?: FormModel['translations']

  @Field(type => [GraphQLJSON], { nullable: true })
  hiddenFields?: HiddenField[]

  @Field(type => [GraphQLJSON], { nullable: true })
  logics?: Logic[]

  @Field(type => [GraphQLJSON], { nullable: true })
  variables?: Variable[]

  @Field({ nullable: true, defaultValue: 0 })
  fieldsUpdatedAt?: number

  @Field({ nullable: true })
  retentionAt?: number

  @Field({ nullable: true })
  suspended?: boolean

  @Field({ nullable: true })
  isDraft?: boolean

  @Field({ nullable: true })
  status?: number

  @Field({ nullable: true })
  version?: number
}
