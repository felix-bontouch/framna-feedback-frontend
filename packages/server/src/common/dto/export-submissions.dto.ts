import { IsNumber, IsOptional, IsString } from 'class-validator'

export class ExportSubmissionsDto {
  @IsString()
  formId: string

  @IsOptional()
  @IsNumber()
  start?: number

  @IsOptional()
  @IsNumber()
  end?: number

  @IsOptional()
  @IsString()
  kind?: string
}
