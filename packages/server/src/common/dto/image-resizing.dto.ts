import { IsNumber, IsOptional, IsString } from 'class-validator'

export class ImageResizingDto {
  @IsString()
  url: string

  @IsOptional()
  w?: string | number

  @IsOptional()
  h?: string | number

  @IsOptional()
  @IsNumber()
  width?: number

  @IsOptional()
  @IsNumber()
  height?: number

  @IsOptional()
  @IsString()
  quality?: string
}
