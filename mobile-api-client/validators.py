"""Field validators for Mobile API Client"""

from typing import Any, Dict, Optional
from exceptions import ValidationError
from utils import validate_email, validate_url, validate_phone


class FieldValidator:
    """Base validator for field validation"""
    
    @staticmethod
    def validate_required(field: Dict, value: Any) -> None:
        """Check if required field has a value"""
        validations = field.get('validations', {})
        if validations.get('required', False):
            if value is None or value == '' or value == []:
                raise ValidationError(
                    "This field is required",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field['kind']
                )
    
    @staticmethod
    def validate_text_length(field: Dict, value: str) -> None:
        """Validate text length constraints"""
        if not isinstance(value, str):
            return
        
        validations = field.get('validations', {})
        min_length = validations.get('minLength')
        max_length = validations.get('maxLength')
        
        if min_length is not None and len(value) < min_length:
            raise ValidationError(
                f"Text must be at least {min_length} characters",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                f"Text must be no more than {max_length} characters",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
    
    @staticmethod
    def validate_number_range(field: Dict, value: Any) -> None:
        """Validate number range constraints"""
        if not isinstance(value, (int, float)):
            return
        
        validations = field.get('validations', {})
        min_value = validations.get('min')
        max_value = validations.get('max')
        
        if min_value is not None and value < min_value:
            raise ValidationError(
                f"Value must be at least {min_value}",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        if max_value is not None and value > max_value:
            raise ValidationError(
                f"Value must be no more than {max_value}",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )


class TextFieldValidator(FieldValidator):
    """Validator for text fields"""
    
    @classmethod
    def validate(cls, field: Dict, value: Any) -> Any:
        """Validate text field value"""
        cls.validate_required(field, value)
        
        if value is None or value == '':
            return None if not field.get('validations', {}).get('required') else ''
        
        if not isinstance(value, str):
            value = str(value)
        
        cls.validate_text_length(field, value)
        
        # Field-specific validation
        field_kind = field['kind']
        
        if field_kind == 'email' and value:
            if not validate_email(value):
                raise ValidationError(
                    "Please enter a valid email address",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field_kind,
                    value=value
                )
        
        elif field_kind == 'website' and value:
            if not validate_url(value):
                raise ValidationError(
                    "Please enter a valid URL",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field_kind,
                    value=value
                )
        
        return value


class ChoiceFieldValidator(FieldValidator):
    """Validator for choice fields"""
    
    @classmethod
    def validate(cls, field: Dict, value: Any) -> Dict:
        """Validate choice field value"""
        properties = field.get('properties', {})
        choices = properties.get('choices', [])
        allow_multiple = properties.get('allowMultiple', False)
        allow_other = properties.get('allowOther', False)
        
        # Handle None or empty
        if value is None or value == {}:
            cls.validate_required(field, None)
            return {"value": []}
        
        # Ensure value is a dict with correct structure
        if not isinstance(value, dict):
            # Convert simple format to expected format
            if isinstance(value, list):
                value = {"value": value}
            elif isinstance(value, str):
                value = {"value": [value]}
            else:
                raise ValidationError(
                    "Invalid choice field format",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field['kind'],
                    value=value
                )
        
        # Validate value array
        selected_choices = value.get('value', [])
        if not isinstance(selected_choices, list):
            selected_choices = [selected_choices] if selected_choices else []
        
        # Check for valid choice IDs
        valid_choice_ids = [c['id'] for c in choices]
        for choice_id in selected_choices:
            if choice_id not in valid_choice_ids:
                raise ValidationError(
                    f"Invalid choice: {choice_id}",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field['kind'],
                    value=value
                )
        
        # Check multiple selection
        if not allow_multiple and len(selected_choices) > 1:
            raise ValidationError(
                "Multiple selection is not allowed",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        # Check other option
        other_value = value.get('other')
        if other_value and not allow_other:
            raise ValidationError(
                "Other option is not allowed",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        # Check required
        if not selected_choices and not other_value:
            cls.validate_required(field, None)
        
        # Build final value
        result = {"value": selected_choices}
        if other_value:
            result["other"] = other_value
        
        return result


class BooleanFieldValidator(FieldValidator):
    """Validator for boolean fields"""
    
    @classmethod
    def validate(cls, field: Dict, value: Any) -> Any:
        """Validate boolean field value"""
        cls.validate_required(field, value)
        
        if value is None:
            return False
        
        # For yes_no fields, we need to preserve the choice ID
        if field.get('kind') == 'yes_no':
            # Check if it's a valid choice ID
            choices = field.get('properties', {}).get('choices', [])
            choice_ids = [c.get('id') for c in choices]
            
            if value in choice_ids:
                return value  # Return the choice ID as-is
            
            # If it's a boolean, convert to appropriate choice ID
            if isinstance(value, bool) or (isinstance(value, str) and value.lower() in ('true', 'false', 'yes', 'no')):
                # Find Yes and No choice IDs
                yes_choice = None
                no_choice = None
                for choice in choices:
                    label = choice.get('label', '').lower()
                    if 'yes' in label:
                        yes_choice = choice.get('id')
                    elif 'no' in label:
                        no_choice = choice.get('id')
                
                # Convert boolean to choice ID
                if isinstance(value, bool):
                    return yes_choice if value else no_choice
                elif isinstance(value, str):
                    is_yes = value.lower() in ('true', 'yes')
                    return yes_choice if is_yes else no_choice
            
            # Invalid value
            raise ValidationError(
                "Please choose you choice",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        # For legal and other boolean fields, convert to boolean
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1')
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        return False


class NumberFieldValidator(FieldValidator):
    """Validator for number fields"""
    
    @classmethod
    def validate(cls, field: Dict, value: Any) -> Optional[float]:
        """Validate number field value"""
        cls.validate_required(field, value)
        
        if value is None or value == '':
            return None
        
        try:
            num_value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(
                "Please enter a valid number",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        cls.validate_number_range(field, num_value)
        
        # For rating/scale fields, validate against total
        if field['kind'] in ('rating', 'opinion_scale'):
            total = field.get('properties', {}).get('total', 5)
            if num_value < 1 or num_value > total:
                raise ValidationError(
                    f"Value must be between 1 and {total}",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field['kind'],
                    value=value
                )
        
        # Return int for whole numbers
        if num_value == int(num_value):
            return int(num_value)
        
        return num_value


class DateFieldValidator(FieldValidator):
    """Validator for date fields"""
    
    @classmethod
    def validate(cls, field: Dict, value: Any) -> Optional[str]:
        """Validate date field value"""
        cls.validate_required(field, value)
        
        if value is None or value == '':
            return None
        
        # Accept string dates in various formats
        if isinstance(value, str):
            import re
            # Accept ISO format (YYYY-MM-DD)
            if re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                return value
            # Accept US format (MM/DD/YYYY) 
            elif re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', value):
                return value
            # Accept other common date formats
            else:
                # For now, just return the value as-is and let the server validate
                return value
        
        # Convert date objects to string
        from datetime import date, datetime
        if isinstance(value, datetime):
            # Use US format for date objects
            return value.strftime("%m/%d/%Y")
        elif isinstance(value, date):
            # Use US format for date objects
            return value.strftime("%m/%d/%Y")
        
        raise ValidationError(
            "Invalid date format",
            field_id=field['id'],
            field_title=field.get('title'),
            field_kind=field['kind'],
            value=value
        )


class PhoneFieldValidator(FieldValidator):
    """Validator for phone number fields"""
    
    @classmethod
    def validate(cls, field: Dict, value: Any) -> Optional[str]:
        """Validate phone number field value"""
        cls.validate_required(field, value)
        
        if value is None or value == '':
            return None
        
        value = str(value).strip()
        
        # Must include country code
        if not value.startswith('+'):
            raise ValidationError(
                "Phone number must include country code (e.g., +1234567890)",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        if not validate_phone(value):
            raise ValidationError(
                "Please enter a valid phone number with country code",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        return value


class ComplexFieldValidator(FieldValidator):
    """Validator for complex field types"""
    
    @classmethod
    def validate_address(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Validate address field"""
        cls.validate_required(field, value)
        
        if value is None or value == {}:
            return None
        
        if not isinstance(value, dict):
            raise ValidationError(
                "Address must be a dictionary",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        # Required address fields
        required_fields = ['address1', 'city', 'state', 'zip', 'country']
        for req_field in required_fields:
            if req_field not in value or not value[req_field]:
                raise ValidationError(
                    f"Address field '{req_field}' is required",
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field['kind'],
                    value=value
                )
        
        return value
    
    @classmethod
    def validate_full_name(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Validate full name field"""
        cls.validate_required(field, value)
        
        if value is None or value == {}:
            return None
        
        if isinstance(value, str):
            # Split string into first and last name
            parts = value.strip().split(None, 1)
            if len(parts) == 2:
                value = {"firstName": parts[0], "lastName": parts[1]}
            else:
                value = {"firstName": parts[0], "lastName": ""}
        
        if not isinstance(value, dict):
            raise ValidationError(
                "Full name must be a dictionary with firstName and lastName",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        if 'firstName' not in value or not value['firstName']:
            raise ValidationError(
                "First name is required",
                field_id=field['id'],
                field_title=field.get('title'),
                field_kind=field['kind'],
                value=value
            )
        
        return value


def validate_field(field: Dict, value: Any) -> Any:
    """Main validation function - routes to appropriate validator"""
    field_kind = field['kind']
    
    # Text fields
    if field_kind in ('short_text', 'long_text', 'email', 'website'):
        return TextFieldValidator.validate(field, value)
    
    # Choice fields
    elif field_kind in ('multiple_choice', 'dropdown', 'picture_choice'):
        return ChoiceFieldValidator.validate(field, value)
    
    # Boolean fields
    elif field_kind in ('yes_no', 'legal'):
        return BooleanFieldValidator.validate(field, value)
    
    # Number fields
    elif field_kind in ('number', 'rating', 'opinion_scale'):
        return NumberFieldValidator.validate(field, value)
    
    # Date fields
    elif field_kind in ('date', 'time'):
        return DateFieldValidator.validate(field, value)
    
    # Phone field
    elif field_kind == 'phone_number':
        return PhoneFieldValidator.validate(field, value)
    
    # Address field
    elif field_kind == 'address':
        return ComplexFieldValidator.validate_address(field, value)
    
    # Full name field
    elif field_kind == 'full_name':
        return ComplexFieldValidator.validate_full_name(field, value)
    
    # For unsupported or custom fields, return as-is
    else:
        FieldValidator.validate_required(field, value)
        return value