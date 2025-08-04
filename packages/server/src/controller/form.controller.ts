import { Controller, Get, Res } from '@nestjs/common'
import { Response } from 'express'

import {
  APP_HOMEPAGE_URL,
  COOKIE_DOMAIN,
  GEETEST_CAPTCHA_KEY,
  GOOGLE_RECAPTCHA_KEY
} from '@environments'

@Controller()
export class FormController {
  @Get('/form/:formId')
  async index(@Res() res: Response) {
    return res.render('index', {
      heyform: {
        homepageURL: APP_HOMEPAGE_URL,
        websiteURL: APP_HOMEPAGE_URL,
        cookieDomain: COOKIE_DOMAIN,
        geetestCaptchaId: GEETEST_CAPTCHA_KEY,
        googleRecaptchaKey: GOOGLE_RECAPTCHA_KEY
      }
    })
  }
}
