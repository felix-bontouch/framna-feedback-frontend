import { getTheme, getThemeStyle, getWebFontURL } from '@heyform-inc/form-renderer/src'
import { CaptchaKindEnum } from '@heyform-inc/shared-types-enums'

import { alpha, darken, helper, isDarkColor, lighten, toURLQuery } from '@heyform-inc/utils'

const APP_NAME = 'HeyForm'
const APP_DESCRIPTION =
  'Build elegant, clean customized forms according to your requirements. Easy to build drag and drop form buider. Create online forms with event feedback form template, exam registration form template, customer satisfaction survey template, event feedback form template, and more.'

const APP_FAVICON_URL = 'https://forms.b-cdn.net/website/favicon.png'

const GoogleAnalytics = ({ apiKey }: { apiKey: string }) => {
  return (
    <>
      <script async src={`https://www.googletagmanager.com/gtag/js?id=${apiKey}`} />
      <script
        dangerouslySetInnerHTML={{
          __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${apiKey}');`
        }}
      />
    </>
  )
}

const FacebookPixel = ({ apiKey }: { apiKey: string }) => {
  return (
    <script
      dangerouslySetInnerHTML={{
        __html: `
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
              n.callMethod.apply(n,arguments):n.queue.push(arguments)};
              if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
              n.queue=[];t=b.createElement(e);t.async=!0;
              t.src=v;s=b.getElementsByTagName(e)[0];
              s.parentNode.insertBefore(t,s)}(window, document,'script',
              'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '${apiKey}');
            fbq('track', 'PageView');`
      }}
    />
  )
}

interface ReportHeadProps {
  form: Record<string, Any>
  theme: Record<string, Any>
  active: boolean
}

function getStyle(theme: Record<string, Any>, active: boolean) {
  if (!active) {
    return
  }

  return `
    body {
      font-family: ${theme.fontFamily};
      --heyform-report-background-color: ${theme.backgroundColor};
      --heyform-report-heading: ${theme.heading};
      --heyform-report-heading-a60: ${alpha(theme.heading, 0.6)};
      --heyform-report-question: ${theme.question};
      --heyform-report-question-a60: ${alpha(theme.question, 0.6)};
      --heyform-report-question-a05: ${alpha(theme.question, 0.05)};
      --heyform-report-chart: ${theme.chart};
      --heyform-report-chart-a15: ${alpha(theme.chart, 0.15)};
      --heyform-report-chart-a025: ${alpha(theme.chart, 0.025)};
      --heyform-report-button-text: ${isDarkColor(theme.question) ? lighten(theme.question, 1) : darken(theme.question, 1)};
    }
    
    html, body {
      height: auto !important;
      overflow: auto !important;
    }
  `
}

export function CustomHead({ team, form, integrations, query }: PublicFormType) {
  const theme = getTheme(form.themeSettings?.theme)
  const fontURL = getWebFontURL(theme.fontFamily)
  const publicUrl = `${process.env.NEXT_PUBLIC_FORM_PREFIX}/${form.id}`

  let title = APP_NAME
  let description = APP_DESCRIPTION
  let faviconUrl = APP_FAVICON_URL
  let ogImageUrl = `${process.env.NEXT_PUBLIC_FORM_PREFIX}/api/og/${form.id}?v=${form.version || 0}`

  if (form.settings.active) {
    if (helper.isValid(form.settings?.metaTitle)) {
      title = form.settings.metaTitle
    } else {
      title = helper.isValid(form.name) ? form.name : APP_NAME
    }

    if (helper.isValid(form.settings?.metaDescription)) {
      description = form.settings.metaDescription
    }

    if (team?.avatar) {
      faviconUrl = toURLQuery(
        {
          url: team.avatar,
          w: 32,
          h: 32,
          format: 'png'
        },
        process.env.NEXT_PUBLIC_IMAGE_RESIZE_URL
      )
    }

    if (form.settings?.metaOGImageUrl) {
      ogImageUrl = form.settings.metaOGImageUrl
    }
  }

  return (
    <Head>
      <meta content="width=device-width, initial-scale=1" name="viewport" />
      <meta content="yes" name="mobile-web-app-capable" />
      <meta content="yes" name="apple-mobile-web-app-capable" />
      <meta content="HeyForm" name="application-name" />
      <meta content="white" name="apple-mobile-web-app-status-bar-style" />
      <meta content="HeyForm" name="apple-mobile-web-app-title" />
      <meta content="telephone=no,email=no" name="format-detection" />

      {/* HTML Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />

      {/* Canonical */}
      <link rel="canonical" href={publicUrl} />

      {/* Facebook Meta Tags */}
      <meta property="og:url" content={publicUrl} />
      <meta property="og:type" content="website" />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImageUrl} />

      {/* Twitter Meta Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={publicUrl} />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImageUrl} />

      {/* Favicon Tags */}
      <link rel="icon" href={faviconUrl} sizes="32x32" type="image/png" />

      {/* Styles */}
      <link href={fontURL} rel="stylesheet" />
      <style dangerouslySetInnerHTML={{ __html: getThemeStyle(theme, query) }} />

      {form.settings.captchaKind === CaptchaKindEnum.GOOGLE_RECAPTCHA && (
        <script src={`https://www.google.com/recaptcha/api.js?render=${RECAPTCHA_KEY}`} />
      )}
      {form.settings.captchaKind === CaptchaKindEnum.GEETEST_CAPTCHA && (
        <script src="https://static.geetest.com/v4/gt4.js" />
      )}

      {helper.isValid(integrations.googleanalytics) && (
        <GoogleAnalytics apiKey={integrations.googleanalytics} />
      )}
      {helper.isValid(integrations.facebookpixel) && (
        <FacebookPixel apiKey={integrations.facebookpixel} />
      )}
    </Head>
  )
}
