"""Utility functions for response generator"""

from typing import Any, Union, List


def get_field_text(field_value: Union[str, List[str], None]) -> str:
    """
    Extract text from field value that might be string or array.
    The API returns title and description as arrays, but we need strings.
    
    Args:
        field_value: Can be a string, list of strings, or None
    
    Returns:
        String value, empty string if None or empty list
    """
    if isinstance(field_value, list):
        # Join array elements with space if multiple, or return first element
        if field_value:
            return ' '.join(field_value) if len(field_value) > 1 else field_value[0]
        return ''
    return field_value or ''