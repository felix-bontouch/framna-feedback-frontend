import {
  BadRequestException,
  Body,
  Controller,
  Get,
  HttpCode,
  HttpStatus,
  Param,
  Post,
  Put,
  Query
} from '@nestjs/common'

import { MobileFieldsQueryDto, MobileSubmissionRequestDto, MobileSubmissionResponseDto } from '@dto'
import { timestamp } from '@heyform-inc/utils'
import { FormService, MobileFormService } from '@service'

@Controller('api/mobile/forms')
export class MobileFormsController {
  constructor(
    private readonly formService: FormService,
    private readonly mobileFormService: MobileFormService
  ) {}

  @Get(':formId')
  async getForm(@Param('formId') formId: string): Promise<any> {
    const form = await this.formService.findPublicForm(formId)

    if (!form) {
      throw new BadRequestException('Form not found')
    }

    if (form.suspended) {
      throw new BadRequestException('Form is suspended')
    }

    if (form.settings?.active !== true) {
      throw new BadRequestException('Form is not active')
    }

    // Transform form for mobile consumption
    return this.mobileFormService.transformFormForMobile(form)
  }

  @Get(':formId/fields')
  async getFormFields(
    @Param('formId') formId: string,
    @Query() query: MobileFieldsQueryDto
  ): Promise<any> {
    const form = await this.formService.findPublicForm(formId)

    if (!form) {
      throw new BadRequestException('Form not found')
    }

    if (form.suspended || form.settings?.active !== true) {
      throw new BadRequestException('Form is not accessible')
    }

    // Get specific fields or all fields
    return this.mobileFormService.getFormFields(form, query.fieldIds)
  }

  @Post(':formId')
  @HttpCode(HttpStatus.OK)
  async submitForm(
    @Param('formId') formId: string,
    @Body() submissionDto: MobileSubmissionRequestDto
  ): Promise<MobileSubmissionResponseDto> {
    const form = await this.formService.findPublicForm(formId)

    if (!form) {
      throw new BadRequestException('Form not found')
    }

    if (form.suspended) {
      throw new BadRequestException('Form is suspended')
    }

    if (form.settings?.active !== true) {
      throw new BadRequestException('Form is not active')
    }

    // Submit the form using the mobile form service
    const result = await this.mobileFormService.submitForm(form, submissionDto)

    return {
      success: true,
      submissionId: result.submissionId,
      timestamp: timestamp(),
      redirectUrl: form.settings?.redirectUrl,
      message: 'Form submitted successfully'
    }
  }

  @Get(':formId/share')
  async getFormShareInfo(@Param('formId') formId: string): Promise<any> {
    const form = await this.formService.findPublicForm(formId)

    if (!form) {
      throw new BadRequestException('Form not found')
    }

    return this.mobileFormService.getFormShareInfo(form)
  }

  @Put(':formId/settings')
  @HttpCode(HttpStatus.OK)
  async updateFormSettings(
    @Param('formId') formId: string,
    @Body() settingsDto: any
  ): Promise<any> {
    const form = await this.formService.findById(formId)

    if (!form) {
      throw new BadRequestException('Form not found')
    }

    // Note: In production, this would require authentication
    // For now, we'll allow updates for demonstration
    return this.mobileFormService.updateFormSettings(form, settingsDto)
  }
}
