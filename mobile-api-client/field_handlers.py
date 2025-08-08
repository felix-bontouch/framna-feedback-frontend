"""Field handlers for different field types in Mobile API Client"""

from typing import Any, Dict, Optional, List
import json
from utils import (
    parse_choice_input, 
    format_date, 
    encode_signature_to_base64
)
from validators import validate_field


class FieldHandler:
    """Base handler for field processing"""
    
    @classmethod
    def format(cls, field: Dict, value: Any) -> Any:
        """Format value for API submission"""
        # First validate the value
        validated = validate_field(field, value)
        # Then format it appropriately
        return cls._format_value(field, validated)
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Any:
        """Internal format method to be overridden"""
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Any:
        """Parse user input string to appropriate value"""
        return input_str


class TextFieldHandler(FieldHandler):
    """Handler for text-based fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[str]:
        """Format text value"""
        if value is None or value == '':
            return None
        return str(value)


class ChoiceFieldHandler(FieldHandler):
    """Handler for choice-based fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Dict:
        """Format choice value to required structure"""
        if value is None:
            return {"value": []}
        
        # Already formatted correctly by validator
        if isinstance(value, dict) and 'value' in value:
            return value
        
        # Should not reach here after validation, but handle edge cases
        if isinstance(value, list):
            return {"value": value}
        elif isinstance(value, str):
            return {"value": [value]}
        
        return {"value": []}
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Dict:
        """Parse user input for choice field"""
        properties = field.get('properties', {})
        choices = properties.get('choices', [])
        allow_multiple = properties.get('allowMultiple', False)
        allow_other = properties.get('allowOther', False)
        
        # Check if input contains "other:" prefix
        other_value = None
        if allow_other and input_str.startswith('other:'):
            other_value = input_str[6:].strip()
            return {"value": [], "other": other_value}
        
        # Parse choices
        selected_ids = parse_choice_input(input_str, choices, allow_multiple)
        
        result = {"value": selected_ids}
        if other_value:
            result["other"] = other_value
        
        return result


class BooleanFieldHandler(FieldHandler):
    """Handler for boolean fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Any:
        """Format boolean value"""
        if value is None:
            return False
        
        # For yes_no fields, preserve the choice ID string
        if field.get('kind') == 'yes_no':
            # If it's already a choice ID, return as-is
            choices = field.get('properties', {}).get('choices', [])
            choice_ids = [c.get('id') for c in choices]
            if value in choice_ids:
                return value
            
            # Otherwise convert boolean to choice ID
            yes_choice = None
            no_choice = None
            for choice in choices:
                label = choice.get('label', '').lower()
                if 'yes' in label:
                    yes_choice = choice.get('id')
                elif 'no' in label:
                    no_choice = choice.get('id')
            
            if isinstance(value, bool):
                return yes_choice if value else no_choice
            elif isinstance(value, str) and value.lower() in ('true', 'false', 'yes', 'no'):
                is_yes = value.lower() in ('true', 'yes')
                return yes_choice if is_yes else no_choice
            
            # Default to first choice if unclear
            return choices[0].get('id') if choices else value
        
        # For legal and other boolean fields, convert to boolean
        return bool(value)
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> bool:
        """Parse user input for boolean field"""
        return input_str.lower() in ('true', 'yes', 'y', '1')


class NumberFieldHandler(FieldHandler):
    """Handler for number fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[float]:
        """Format number value"""
        if value is None:
            return None
        
        # Validator already converts to appropriate number type
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[float]:
        """Parse user input for number field"""
        if not input_str:
            return None
        
        try:
            value = float(input_str)
            # Return int for whole numbers
            if value == int(value):
                return int(value)
            return value
        except ValueError:
            raise ValueError(f"Invalid number: {input_str}")


class DateFieldHandler(FieldHandler):
    """Handler for date fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[str]:
        """Format date value"""
        if value is None:
            return None
        
        # Return the date value as-is (validator accepts multiple formats)
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[str]:
        """Parse user input for date field"""
        if not input_str:
            return None
        
        # Accept various formats - return as-is
        # The validator and server will handle format validation
        return input_str


class DateRangeFieldHandler(FieldHandler):
    """Handler for date range fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Format date range value"""
        if value is None:
            return None
        
        if isinstance(value, dict):
            return {
                "start": format_date(value.get('start')),
                "end": format_date(value.get('end'))
            }
        
        return None
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[Dict]:
        """Parse user input for date range field"""
        if not input_str:
            return None
        
        # Expect format: "2024-01-01 to 2024-01-31"
        parts = input_str.split(' to ')
        if len(parts) != 2:
            raise ValueError("Date range must be in format: YYYY-MM-DD to YYYY-MM-DD")
        
        try:
            from dateutil import parser
            start = parser.parse(parts[0].strip()).date().isoformat()
            end = parser.parse(parts[1].strip()).date().isoformat()
            return {"start": start, "end": end}
        except Exception:
            return {"start": parts[0].strip(), "end": parts[1].strip()}


class PhoneFieldHandler(FieldHandler):
    """Handler for phone number fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[str]:
        """Format phone number value"""
        if value is None:
            return None
        
        # Validator already ensures correct format
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[str]:
        """Parse user input for phone field"""
        if not input_str:
            return None
        
        # Ensure country code is included
        phone = input_str.strip()
        if not phone.startswith('+'):
            # Try to add default country code if specified
            default_code = field.get('properties', {}).get('defaultCountryCode', '+1')
            if not default_code.startswith('+'):
                default_code = '+' + default_code
            phone = default_code + phone
        
        return phone


class AddressFieldHandler(FieldHandler):
    """Handler for address fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Format address value"""
        if value is None:
            return None
        
        # Validator already ensures correct structure
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[Dict]:
        """Parse user input for address field"""
        if not input_str:
            return None
        
        # Try to parse JSON first
        try:
            return json.loads(input_str)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Otherwise expect comma-separated format
        # "123 Main St, Apt 4B, New York, NY, 10001, US"
        parts = [p.strip() for p in input_str.split(',')]
        
        if len(parts) < 5:
            raise ValueError("Address must include: address1, city, state, zip, country")
        
        address = {
            "address1": parts[0],
            "city": parts[-4] if len(parts) > 5 else parts[1],
            "state": parts[-3] if len(parts) > 5 else parts[2],
            "zip": parts[-2] if len(parts) > 5 else parts[3],
            "country": parts[-1] if len(parts) > 5 else parts[4]
        }
        
        if len(parts) > 5:
            address["address2"] = ', '.join(parts[1:-4])
        
        return address


class FullNameFieldHandler(FieldHandler):
    """Handler for full name fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Format full name value"""
        if value is None:
            return None
        
        # Validator already ensures correct structure
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[Dict]:
        """Parse user input for full name field"""
        if not input_str:
            return None
        
        # Try JSON first
        try:
            return json.loads(input_str)
        except:
            pass
        
        # Split into first and last name
        parts = input_str.strip().split(None, 1)
        if len(parts) == 2:
            return {"firstName": parts[0], "lastName": parts[1]}
        else:
            return {"firstName": parts[0], "lastName": ""}


class FileUploadFieldHandler(FieldHandler):
    """Handler for file upload fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Format file upload value"""
        if value is None:
            return None
        
        if isinstance(value, dict):
            # Ensure required fields
            required = ['url', 'name', 'size', 'type']
            if all(k in value for k in required):
                return value
        
        return None
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[Dict]:
        """Parse user input for file upload field"""
        if not input_str:
            return None
        
        # Expect JSON format
        try:
            return json.loads(input_str)
        except (json.JSONDecodeError, ValueError):
            # Or URL with metadata
            return {
                "url": input_str,
                "name": input_str.split('/')[-1],
                "size": 0,
                "type": "application/octet-stream"
            }


class SignatureFieldHandler(FieldHandler):
    """Handler for signature fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[str]:
        """Format signature value"""
        if value is None:
            return None
        
        # If it's a file path, encode it
        if isinstance(value, str) and not value.startswith('data:'):
            try:
                return encode_signature_to_base64(value)
            except Exception:
                pass
        
        return value
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[str]:
        """Parse user input for signature field"""
        if not input_str:
            return None
        
        # If it's a file path, encode it
        if not input_str.startswith('data:'):
            return encode_signature_to_base64(input_str)
        
        return input_str


class CountryFieldHandler(FieldHandler):
    """Handler for country fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[str]:
        """Format country value"""
        if value is None:
            return None
        
        # Should be ISO 3166-1 alpha-2 code
        return str(value).upper()[:2]
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[str]:
        """Parse user input for country field"""
        if not input_str:
            return None
        
        # Accept 2-letter country code
        return input_str.upper()[:2]


class InputTableFieldHandler(FieldHandler):
    """Handler for input table fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[List]:
        """Format input table value"""
        if value is None:
            return None
        
        if isinstance(value, list):
            return value
        
        return None
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[List]:
        """Parse user input for input table field"""
        if not input_str:
            return None
        
        # Expect JSON array format
        try:
            return json.loads(input_str)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Input table must be a JSON array: {e}")


class MatrixFieldHandler(FieldHandler):
    """Handler for matrix fields"""
    
    @classmethod
    def _format_value(cls, field: Dict, value: Any) -> Optional[Dict]:
        """Format matrix value"""
        if value is None:
            return None
        
        if isinstance(value, dict):
            return value
        
        return None
    
    @classmethod
    def parse_input(cls, field: Dict, input_str: str) -> Optional[Dict]:
        """Parse user input for matrix field"""
        if not input_str:
            return None
        
        # Expect JSON object format
        try:
            return json.loads(input_str)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Matrix must be a JSON object: {e}")


# Field handler registry
FIELD_HANDLERS = {
    'short_text': TextFieldHandler,
    'long_text': TextFieldHandler,
    'email': TextFieldHandler,
    'website': TextFieldHandler,
    'multiple_choice': ChoiceFieldHandler,
    'dropdown': ChoiceFieldHandler,
    'picture_choice': ChoiceFieldHandler,
    'yes_no': BooleanFieldHandler,
    'legal': BooleanFieldHandler,
    'number': NumberFieldHandler,
    'rating': NumberFieldHandler,
    'opinion_scale': NumberFieldHandler,
    'date': DateFieldHandler,
    'date_range': DateRangeFieldHandler,
    'time': DateFieldHandler,
    'phone_number': PhoneFieldHandler,
    'address': AddressFieldHandler,
    'full_name': FullNameFieldHandler,
    'file_upload': FileUploadFieldHandler,
    'signature': SignatureFieldHandler,
    'country': CountryFieldHandler,
    'input_table': InputTableFieldHandler,
    'matrix': MatrixFieldHandler
}


def get_field_handler(field_kind: str) -> FieldHandler:
    """Get the appropriate handler for a field type"""
    return FIELD_HANDLERS.get(field_kind, FieldHandler)


def format_answer(field: Dict, value: Any) -> Any:
    """Format an answer value for a specific field"""
    handler = get_field_handler(field['kind'])
    return handler.format(field, value)


def parse_field_input(field: Dict, input_str: str) -> Any:
    """Parse user input for a specific field"""
    handler = get_field_handler(field['kind'])
    return handler.parse_input(field, input_str)