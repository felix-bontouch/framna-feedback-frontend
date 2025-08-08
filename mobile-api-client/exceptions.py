"""Custom exceptions for Mobile API Client"""


class MobileAPIError(Exception):
    """Base exception for Mobile API Client"""
    pass


class FormNotFoundError(MobileAPIError):
    """Raised when a form is not found"""
    def __init__(self, form_id: str):
        self.form_id = form_id
        super().__init__(f"Form not found: {form_id}")


class FormInactiveError(MobileAPIError):
    """Raised when a form is not active or suspended"""
    def __init__(self, form_id: str, reason: str = "Form is not active"):
        self.form_id = form_id
        self.reason = reason
        super().__init__(f"Form {form_id}: {reason}")


class ValidationError(MobileAPIError):
    """Raised when field validation fails"""
    def __init__(self, message: str, field_id: str = None, field_title: str = None,
                 field_kind: str = None, value: any = None):
        self.field_id = field_id
        self.field_title = field_title
        self.field_kind = field_kind
        self.value = value
        self.message = message
        
        error_msg = message
        if field_title:
            error_msg = f"Field '{field_title}': {message}"
        elif field_id:
            error_msg = f"Field '{field_id}': {message}"
        
        super().__init__(error_msg)


class QuotaExceededError(MobileAPIError):
    """Raised when submission quota is exceeded"""
    def __init__(self, form_id: str):
        self.form_id = form_id
        super().__init__(f"Submission quota exceeded for form: {form_id}")


class RateLimitError(MobileAPIError):
    """Raised when API rate limit is hit"""
    def __init__(self, retry_after: int = None):
        self.retry_after = retry_after
        msg = "API rate limit exceeded"
        if retry_after:
            msg += f". Retry after {retry_after} seconds"
        super().__init__(msg)


class PasswordRequiredError(MobileAPIError):
    """Raised when a form requires a password"""
    def __init__(self, form_id: str):
        self.form_id = form_id
        super().__init__(f"Password required for form: {form_id}")


class CaptchaRequiredError(MobileAPIError):
    """Raised when a form requires captcha verification"""
    def __init__(self, form_id: str, captcha_kind: str):
        self.form_id = form_id
        self.captcha_kind = captcha_kind
        super().__init__(f"Captcha verification required for form: {form_id} (type: {captcha_kind})")