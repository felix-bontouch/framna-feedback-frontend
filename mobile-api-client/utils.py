"""Utility functions for Mobile API Client"""

import base64
import json
import platform
import socket
import time
import uuid
from datetime import datetime, date
from typing import Dict, Any, Optional
import locale


def get_device_info() -> Dict[str, str]:
    """Get device information for client info"""
    return {
        "os": platform.system(),
        "osVersion": platform.release(),
        "appVersion": "1.0.0",  # You can make this configurable
        "device": platform.machine(),
        "deviceId": str(uuid.uuid4()),
        "locale": locale.getdefaultlocale()[0] or "en_US"
    }


def get_device_ip() -> str:
    """Get the device's IP address"""
    try:
        # Connect to a public DNS server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_user_agent() -> str:
    """Generate a user agent string"""
    return f"MobileAPIClient/1.0 ({platform.system()} {platform.release()}; Python {platform.python_version()})"


def format_date(date_obj: Any, format_str: str = None) -> str:
    """Format a date object to string"""
    if isinstance(date_obj, str):
        return date_obj
    
    if format_str:
        if isinstance(date_obj, (datetime, date)):
            return date_obj.strftime(format_str)
    
    if isinstance(date_obj, datetime):
        return date_obj.date().isoformat()
    elif isinstance(date_obj, date):
        return date_obj.isoformat()
    
    return str(date_obj)


def encode_signature_to_base64(image_path: str) -> str:
    """Encode an image file to base64 data URL"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Determine MIME type based on file extension
        if image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        elif image_path.lower().endswith(('.jpg', '.jpeg')):
            mime_type = 'image/jpeg'
        else:
            mime_type = 'image/png'  # Default to PNG
        
        base64_data = base64.b64encode(image_data).decode('utf-8')
        return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        raise ValueError(f"Failed to encode signature image: {e}")


def generate_timestamp() -> int:
    """Generate current timestamp in milliseconds"""
    return int(time.time() * 1000)


def pretty_print_json(data: Any) -> None:
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2, default=str))


def extract_field_ids(fields: list) -> list:
    """Extract all field IDs from a form's field list (including nested fields)"""
    field_ids = []
    
    def extract_recursive(field_list):
        for field in field_list:
            field_ids.append(field['id'])
            # Check for nested fields (in GROUP fields)
            if 'properties' in field and 'fields' in field.get('properties', {}):
                extract_recursive(field['properties']['fields'])
    
    extract_recursive(fields)
    return field_ids


def build_client_info(custom_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Build client info object with defaults and custom overrides"""
    default_info = get_device_info()
    default_info.update({
        "ip": get_device_ip(),
        "userAgent": get_user_agent()
    })
    
    if custom_info:
        default_info.update(custom_info)
    
    return default_info


def parse_choice_input(input_str: str, choices: list, allow_multiple: bool = False) -> list:
    """Parse user input for choice fields"""
    # Input can be:
    # - Choice label (e.g., "Very Satisfied")
    # - Choice ID (e.g., "choice1")
    # - Choice number (e.g., "1" for first choice)
    # - Multiple separated by comma (if allow_multiple)
    
    if not input_str:
        return []
    
    selected = []
    
    if allow_multiple:
        parts = [p.strip() for p in input_str.split(',')]
    else:
        parts = [input_str.strip()]
    
    for part in parts:
        # Try to match by label
        for choice in choices:
            if choice.get('label', '').lower() == part.lower():
                selected.append(choice['id'])
                break
        else:
            # Try to match by ID
            if any(c['id'] == part for c in choices):
                selected.append(part)
            # Try to match by number (1-indexed)
            elif part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(choices):
                    selected.append(choices[idx]['id'])
    
    return selected


def format_error_response(error_data: dict) -> str:
    """Format error response for display"""
    lines = []
    
    if 'message' in error_data:
        lines.append(f"Error: {error_data['message']}")
    
    if 'field' in error_data:
        lines.append(f"Field ID: {error_data['field']}")
    
    if 'fieldTitle' in error_data:
        lines.append(f"Field: {error_data['fieldTitle']}")
    
    if 'fieldKind' in error_data:
        lines.append(f"Type: {error_data['fieldKind']}")
    
    if 'value' in error_data:
        lines.append(f"Value provided: {error_data['value']}")
    
    return '\n'.join(lines)


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_url(url: str) -> bool:
    """Basic URL validation"""
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None


def validate_phone(phone: str) -> bool:
    """Basic phone number validation (must include country code)"""
    import re
    # Must start with + and contain only digits, spaces, dashes, parentheses
    pattern = r'^\+[\d\s\-()]+$'
    return re.match(pattern, phone) is not None and len(phone) >= 10