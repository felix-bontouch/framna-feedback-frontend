"""Field-specific generators for different field types"""

import random
import string
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .sentiment_engine import SentimentEngine, Sentiment
from .data_providers import DataProvider
from .personas import Persona
from .utils import get_field_text


class FieldGenerator:
    """Base class for field-specific value generation"""
    
    def __init__(self, sentiment_engine: SentimentEngine, 
                 data_provider: DataProvider,
                 persona: Optional[Persona] = None):
        self.sentiment_engine = sentiment_engine
        self.data_provider = data_provider
        self.persona = persona
    
    def generate(self, field: Dict[str, Any]) -> Any:
        """Generate value for field"""
        raise NotImplementedError
    
    def add_typos(self, text: str, rate: float = 0.02) -> str:
        """Add realistic typos to text"""
        if random.random() > rate:
            return text
        
        text_list = list(text)
        typo_types = ['swap', 'duplicate', 'missing', 'wrong']
        typo_type = random.choice(typo_types)
        
        if len(text_list) > 2:
            pos = random.randint(1, len(text_list) - 2)
            
            if typo_type == 'swap' and pos < len(text_list) - 1:
                # Swap adjacent characters
                text_list[pos], text_list[pos + 1] = text_list[pos + 1], text_list[pos]
            elif typo_type == 'duplicate':
                # Duplicate a character
                text_list.insert(pos, text_list[pos])
            elif typo_type == 'missing' and len(text_list) > 3:
                # Remove a character
                del text_list[pos]
            elif typo_type == 'wrong':
                # Wrong character (nearby on keyboard)
                if text_list[pos].isalpha():
                    nearby = 'qwert' if text_list[pos] in 'qwert' else 'asdfg'
                    text_list[pos] = random.choice(nearby)
        
        return ''.join(text_list)


class TextFieldGenerator(FieldGenerator):
    """Generator for text fields"""
    
    def generate(self, field: Dict[str, Any]) -> str:
        """Generate text based on field context and sentiment"""
        field_kind = field.get('kind', 'short_text')
        title = get_field_text(field.get('title', 'text field')).lower()
        validations = field.get('validations', {})
        
        min_length = validations.get('minLength', 1)
        max_length = validations.get('maxLength', 500)
        
        # Check if it's asking for specific information
        if any(word in title for word in ['name', 'first name', 'last name']):
            if self.persona:
                if 'first' in title:
                    return self.persona.first_name
                elif 'last' in title:
                    return self.persona.last_name
                else:
                    return f"{self.persona.first_name} {self.persona.last_name}"
            else:
                return self.data_provider.get_first_name() + " " + self.data_provider.get_last_name()
        
        elif 'email' in title or field_kind == 'email':
            if self.persona:
                return self.persona.email
            else:
                return self.data_provider.get_email()
        
        elif 'phone' in title or field_kind == 'phone_number':
            if self.persona:
                return self.persona.phone
            else:
                return self.data_provider.get_phone()
        
        elif 'website' in title or 'url' in title or field_kind == 'website':
            return self.data_provider.get_website()
        
        elif 'company' in title or 'organization' in title:
            if self.persona:
                return self.persona.company
            else:
                return self.data_provider.get_company_name()
        
        elif 'address' in title:
            addr = self.data_provider.get_address()
            return f"{addr['address1']}, {addr['city']}, {addr['state']} {addr['zip']}"
        
        else:
            # Generate sentiment-aware text
            if field_kind == 'long_text' or 'comment' in title or 'feedback' in title:
                # Longer text for feedback fields
                text = self.sentiment_engine.generate_text(
                    get_field_text(field.get('title', 'feedback')),
                    min_length=max(min_length, 50),
                    max_length=max_length
                )
            else:
                # Shorter text for regular fields
                text = self.sentiment_engine.generate_text(
                    get_field_text(field.get('title', 'response')),
                    min_length=min_length,
                    max_length=min(max_length, 100)
                )
            
            # Add typos if persona has high error rate
            if self.persona and self.persona.should_make_typo():
                text = self.add_typos(text, self.persona.error_rate)
            
            return text


class ChoiceFieldGenerator(FieldGenerator):
    """Generator for choice fields"""
    
    def generate(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Generate choice selection based on sentiment"""
        properties = field.get('properties', {})
        choices = properties.get('choices', [])
        allow_multiple = properties.get('allowMultiple', False)
        allow_other = properties.get('allowOther', False)
        
        if not choices:
            return {"value": []}
        
        # Use sentiment engine to select choices
        result = self.sentiment_engine.generate_choice_selection(
            choices, allow_multiple, allow_other
        )
        
        # Sometimes add "other" text if allowed
        if allow_other and 'other' in result and not result.get('other'):
            profile = self.sentiment_engine.get_profile()
            result['other'] = profile.get_phrase('middle')
        
        return result


class BooleanFieldGenerator(FieldGenerator):
    """Generator for boolean fields"""
    
    def generate(self, field: Dict[str, Any]) -> Any:
        """Generate boolean based on sentiment and context"""
        title = get_field_text(field.get('title', '')).lower()
        profile = self.sentiment_engine.get_profile()
        field_kind = field.get('kind', '')
        
        # For yes_no fields, we need to return the choice ID, not a boolean
        if field_kind == 'yes_no':
            choices = field.get('properties', {}).get('choices', [])
            if choices:
                # Find Yes and No choice IDs
                yes_choice = None
                no_choice = None
                for choice in choices:
                    label = choice.get('label', '').lower()
                    if 'yes' in label or 'true' in label:
                        yes_choice = choice.get('id')
                    elif 'no' in label or 'false' in label:
                        no_choice = choice.get('id')
                
                # Determine which to choose based on context and sentiment
                should_be_yes = self._should_be_yes(title, profile)
                
                if should_be_yes and yes_choice:
                    return yes_choice
                elif not should_be_yes and no_choice:
                    return no_choice
                elif choices:
                    # Fallback to first choice if we can't determine
                    return choices[0].get('id')
        
        # For legal and other boolean fields, return actual boolean
        return self._should_be_yes(title, profile)
    
    def _should_be_yes(self, title: str, profile) -> bool:
        """Determine if the answer should be yes/true"""
        # Context-aware generation
        if 'recommend' in title:
            return profile.get_boolean('recommendation')
        elif 'agree' in title or 'accept' in title or 'terms' in title:
            # Usually agree to terms
            return random.random() < 0.95
        elif 'subscribe' in title or 'newsletter' in title:
            # Newsletter subscription based on sentiment
            if self.sentiment_engine.current_sentiment == Sentiment.POSITIVE:
                return random.random() < 0.7
            else:
                return random.random() < 0.3
        elif 'authorized' in title or 'eligible' in title or 'qualified' in title:
            # For eligibility questions, usually yes
            return random.random() < 0.85
        else:
            return profile.get_boolean()


class NumberFieldGenerator(FieldGenerator):
    """Generator for number fields"""
    
    def generate(self, field: Dict[str, Any]) -> float:
        """Generate number based on field type and sentiment"""
        field_kind = field.get('kind', 'number')
        validations = field.get('validations', {})
        properties = field.get('properties', {})
        
        if field_kind in ('rating', 'opinion_scale'):
            # Use sentiment-based rating
            total = properties.get('total', 10)
            profile = self.sentiment_engine.get_profile()
            return profile.get_rating(1, total)
        
        else:
            # Regular number field
            min_val = validations.get('min', 0)
            max_val = validations.get('max', 100)
            
            # Check if it's asking for specific numeric data
            title = get_field_text(field.get('title', '')).lower()
            
            if 'age' in title:
                if self.persona:
                    return self.persona.age
                else:
                    return random.randint(18, 75)
            elif 'quantity' in title or 'amount' in title or 'number of' in title:
                # Tend toward lower numbers
                return random.randint(min_val, min(max_val, 10))
            elif 'price' in title or 'cost' in title or '$' in title:
                # Price-like numbers
                return round(random.uniform(min_val, max_val), 2)
            elif 'year' in title:
                current_year = datetime.now().year
                return random.randint(max(min_val, current_year - 10), 
                                     min(max_val, current_year + 1))
            else:
                # Random within range
                if isinstance(min_val, float) or isinstance(max_val, float):
                    return round(random.uniform(min_val, max_val), 2)
                else:
                    return random.randint(int(min_val), int(max_val))


class DateFieldGenerator(FieldGenerator):
    """Generator for date/time fields"""
    
    def generate(self, field: Dict[str, Any]) -> Any:
        """Generate date/time based on context"""
        field_kind = field.get('kind', 'date')
        title = get_field_text(field.get('title', '')).lower()
        
        if field_kind == 'date':
            # Check field properties for date format
            # Default is MM/DD/YYYY unless field specifies otherwise
            date_format = "US"  # Default to US format
            
            # Context-aware date generation
            if 'birth' in title or 'dob' in title:
                if self.persona:
                    # Calculate birth date from age
                    years_ago = self.persona.age
                    birth_date = datetime.now() - timedelta(days=years_ago * 365)
                    return birth_date.strftime("%m/%d/%Y")
                else:
                    return self.data_provider.get_date(past_days=365 * 60, future_days=0, format=date_format)
            elif 'future' in title or 'next' in title or 'upcoming' in title or 'availability' in title or 'start' in title:
                return self.data_provider.get_date(past_days=0, future_days=365, format=date_format)
            elif 'past' in title or 'last' in title or 'previous' in title:
                return self.data_provider.get_date(past_days=365, future_days=0, format=date_format)
            else:
                # Recent dates for most fields
                return self.data_provider.get_date(past_days=90, future_days=30, format=date_format)
        
        elif field_kind == 'date_range':
            return self.data_provider.get_date_range(format="US")  # Use US format by default
        
        elif field_kind == 'time':
            return self.data_provider.get_time()
        
        return None


class AddressFieldGenerator(FieldGenerator):
    """Generator for address fields"""
    
    def generate(self, field: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete address"""
        if self.persona:
            return self.persona.address
        else:
            return self.data_provider.get_address()


class PhoneFieldGenerator(FieldGenerator):
    """Generator for phone number fields"""
    
    def generate(self, field: Dict[str, Any]) -> str:
        """Generate phone number"""
        if self.persona:
            return self.persona.phone
        else:
            properties = field.get('properties', {})
            default_code = properties.get('defaultCountryCode')
            return self.data_provider.get_phone(default_code)


class FullNameFieldGenerator(FieldGenerator):
    """Generator for full name fields"""
    
    def generate(self, field: Dict[str, Any]) -> Dict[str, str]:
        """Generate full name"""
        if self.persona:
            return {
                "firstName": self.persona.first_name,
                "lastName": self.persona.last_name
            }
        else:
            first, last = self.data_provider.get_full_name()
            return {
                "firstName": first,
                "lastName": last
            }


class FileUploadFieldGenerator(FieldGenerator):
    """Generator for file upload fields"""
    
    def generate(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Generate file metadata"""
        title = get_field_text(field.get('title', '')).lower()
        
        # Determine file type from context
        if 'image' in title or 'photo' in title or 'picture' in title:
            file_type = 'image'
        elif 'spreadsheet' in title or 'excel' in title or 'csv' in title:
            file_type = 'spreadsheet'
        else:
            file_type = 'document'
        
        return self.data_provider.get_file_metadata(file_type)


class SignatureFieldGenerator(FieldGenerator):
    """Generator for signature fields"""
    
    def generate(self, field: Dict[str, Any]) -> str:
        """Generate signature data"""
        return self.data_provider.get_signature_data()


class CountryFieldGenerator(FieldGenerator):
    """Generator for country fields"""
    
    def generate(self, field: Dict[str, Any]) -> str:
        """Generate country code"""
        if self.persona:
            return self.persona.address.get('country', 'US')
        else:
            return self.data_provider.get_country_code()


class InputTableFieldGenerator(FieldGenerator):
    """Generator for input table fields"""
    
    def generate(self, field: Dict[str, Any]) -> List[Dict]:
        """Generate table data"""
        properties = field.get('properties', {})
        columns = properties.get('tableColumns', [])
        
        if not columns:
            return []
        
        # Generate 1-3 rows
        num_rows = random.randint(1, 3)
        rows = []
        
        for _ in range(num_rows):
            row = {}
            for col in columns:
                col_id = col.get('id', f'col_{len(row)}')
                col_title = get_field_text(col.get('title', 'column')).lower()
                
                # Generate appropriate data for column
                if 'name' in col_title:
                    row[col_id] = self.data_provider.get_first_name()
                elif 'email' in col_title:
                    row[col_id] = self.data_provider.get_email()
                elif 'date' in col_title:
                    row[col_id] = self.data_provider.get_date()
                elif 'amount' in col_title or 'price' in col_title:
                    row[col_id] = str(round(random.uniform(10, 1000), 2))
                else:
                    row[col_id] = self.data_provider.get_lorem_ipsum(5)
            
            rows.append(row)
        
        return rows


class MatrixFieldGenerator(FieldGenerator):
    """Generator for matrix fields"""
    
    def generate(self, field: Dict[str, Any]) -> Dict:
        """Generate matrix answers"""
        properties = field.get('properties', {})
        rows = properties.get('rows', [])
        columns = properties.get('columns', [])
        
        if not rows or not columns:
            return {}
        
        matrix_answers = {}
        profile = self.sentiment_engine.get_profile()
        
        for row in rows:
            row_id = row.get('id', str(len(matrix_answers)))
            
            # Select a column based on sentiment
            if self.sentiment_engine.current_sentiment == Sentiment.POSITIVE:
                # Tend toward positive columns (usually last ones)
                col_index = random.choices(
                    range(len(columns)),
                    weights=[0.1] * (len(columns) - 2) + [0.3, 0.5]
                )[0] if len(columns) > 2 else -1
            elif self.sentiment_engine.current_sentiment == Sentiment.NEGATIVE:
                # Tend toward negative columns (usually first ones)
                col_index = random.choices(
                    range(len(columns)),
                    weights=[0.5, 0.3] + [0.1] * (len(columns) - 2)
                )[0] if len(columns) > 2 else 0
            else:
                # Random/middle selection
                col_index = random.randint(0, len(columns) - 1)
            
            matrix_answers[row_id] = columns[col_index].get('id', str(col_index))
        
        return matrix_answers


# Field generator registry
FIELD_GENERATORS = {
    'short_text': TextFieldGenerator,
    'long_text': TextFieldGenerator,
    'email': TextFieldGenerator,
    'website': TextFieldGenerator,
    'multiple_choice': ChoiceFieldGenerator,
    'dropdown': ChoiceFieldGenerator,
    'picture_choice': ChoiceFieldGenerator,
    'yes_no': BooleanFieldGenerator,  # Now handles choice IDs for yes_no
    'legal': BooleanFieldGenerator,
    'number': NumberFieldGenerator,
    'rating': NumberFieldGenerator,
    'opinion_scale': NumberFieldGenerator,
    'date': DateFieldGenerator,
    'date_range': DateFieldGenerator,
    'time': DateFieldGenerator,
    'phone_number': PhoneFieldGenerator,
    'address': AddressFieldGenerator,
    'full_name': FullNameFieldGenerator,
    'file_upload': FileUploadFieldGenerator,
    'signature': SignatureFieldGenerator,
    'country': CountryFieldGenerator,
    'input_table': InputTableFieldGenerator,
    'matrix': MatrixFieldGenerator
}


def get_field_generator(field_kind: str, sentiment_engine: SentimentEngine,
                       data_provider: DataProvider, 
                       persona: Optional[Persona] = None) -> FieldGenerator:
    """Get appropriate generator for field type"""
    generator_class = FIELD_GENERATORS.get(field_kind, FieldGenerator)
    return generator_class(sentiment_engine, data_provider, persona)