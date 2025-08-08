"""Field analyzer for intelligent field analysis and generation"""

import re
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from .utils import get_field_text


class FieldIntent(Enum):
    """Intent/purpose of a field"""
    PERSONAL_INFO = "personal_info"
    CONTACT = "contact"
    FEEDBACK = "feedback"
    RATING = "rating"
    PREFERENCE = "preference"
    DEMOGRAPHIC = "demographic"
    TEMPORAL = "temporal"
    LOCATION = "location"
    AGREEMENT = "agreement"
    QUANTITY = "quantity"
    DESCRIPTION = "description"
    IDENTIFICATION = "identification"
    FINANCIAL = "financial"
    OTHER = "other"


class FieldCategory(Enum):
    """Category of field for sentiment relevance"""
    SENTIMENT_HIGH = "sentiment_high"      # Highly affected by sentiment
    SENTIMENT_MEDIUM = "sentiment_medium"  # Moderately affected
    SENTIMENT_LOW = "sentiment_low"        # Minimally affected
    SENTIMENT_NONE = "sentiment_none"      # Not affected by sentiment


class FieldAnalyzer:
    """Analyzes form fields to understand their intent and relationships"""
    
    # Keywords for intent detection
    INTENT_KEYWORDS = {
        FieldIntent.PERSONAL_INFO: [
            'name', 'first', 'last', 'full name', 'surname', 'given name'
        ],
        FieldIntent.CONTACT: [
            'email', 'phone', 'telephone', 'mobile', 'contact', 'address',
            'street', 'city', 'state', 'zip', 'postal', 'country'
        ],
        FieldIntent.FEEDBACK: [
            'feedback', 'comment', 'suggestion', 'opinion', 'thoughts',
            'experience', 'review', 'testimonial', 'describe', 'explain',
            'tell us', 'share', 'additional', 'anything else'
        ],
        FieldIntent.RATING: [
            'rate', 'rating', 'satisfaction', 'satisfied', 'happy',
            'score', 'scale', 'quality', 'performance', 'excellent',
            'good', 'poor', 'terrible'
        ],
        FieldIntent.PREFERENCE: [
            'prefer', 'favorite', 'like', 'choice', 'select', 'choose',
            'interested', 'preference', 'option'
        ],
        FieldIntent.DEMOGRAPHIC: [
            'age', 'gender', 'sex', 'occupation', 'profession', 'job',
            'education', 'income', 'marital', 'ethnicity', 'race'
        ],
        FieldIntent.TEMPORAL: [
            'date', 'time', 'when', 'day', 'month', 'year', 'period',
            'duration', 'start', 'end', 'from', 'to', 'schedule'
        ],
        FieldIntent.LOCATION: [
            'location', 'where', 'place', 'venue', 'city', 'country',
            'region', 'area', 'branch', 'store', 'office'
        ],
        FieldIntent.AGREEMENT: [
            'agree', 'accept', 'terms', 'conditions', 'policy', 'consent',
            'authorize', 'permission', 'subscribe', 'newsletter'
        ],
        FieldIntent.QUANTITY: [
            'how many', 'number', 'amount', 'quantity', 'count', 'total',
            'size', 'volume', 'frequency'
        ],
        FieldIntent.DESCRIPTION: [
            'describe', 'explain', 'detail', 'elaborate', 'specify',
            'what', 'why', 'how', 'reason'
        ],
        FieldIntent.IDENTIFICATION: [
            'id', 'identifier', 'code', 'reference', 'account', 'member',
            'customer', 'order', 'ticket', 'case'
        ],
        FieldIntent.FINANCIAL: [
            'price', 'cost', 'budget', 'payment', 'amount', 'fee',
            'charge', 'expense', 'salary', 'revenue'
        ]
    }
    
    # Sentiment relevance by field type and intent
    SENTIMENT_RELEVANCE = {
        # High sentiment relevance
        'rating': FieldCategory.SENTIMENT_HIGH,
        'opinion_scale': FieldCategory.SENTIMENT_HIGH,
        'long_text': FieldCategory.SENTIMENT_HIGH,
        
        # Medium sentiment relevance  
        'multiple_choice': FieldCategory.SENTIMENT_MEDIUM,
        'yes_no': FieldCategory.SENTIMENT_MEDIUM,
        'short_text': FieldCategory.SENTIMENT_MEDIUM,
        
        # Low sentiment relevance
        'dropdown': FieldCategory.SENTIMENT_LOW,
        'number': FieldCategory.SENTIMENT_LOW,
        
        # No sentiment relevance
        'email': FieldCategory.SENTIMENT_NONE,
        'phone_number': FieldCategory.SENTIMENT_NONE,
        'date': FieldCategory.SENTIMENT_NONE,
        'address': FieldCategory.SENTIMENT_NONE,
        'full_name': FieldCategory.SENTIMENT_NONE,
        'file_upload': FieldCategory.SENTIMENT_NONE,
        'signature': FieldCategory.SENTIMENT_NONE,
        'country': FieldCategory.SENTIMENT_NONE
    }
    
    def __init__(self):
        self.field_cache = {}
        self.relationships = {}
    
    def analyze_field(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single field to determine its intent and characteristics"""
        field_id = field.get('id')
        
        # Check cache
        if field_id in self.field_cache:
            return self.field_cache[field_id]
        
        analysis = {
            'id': field_id,
            'kind': field.get('kind'),
            'intent': self._detect_intent(field),
            'sentiment_category': self._get_sentiment_category(field),
            'is_required': field.get('validations', {}).get('required', False),
            'constraints': self._extract_constraints(field),
            'keywords': self._extract_keywords(field),
            'is_personal_data': self._is_personal_data(field),
            'is_feedback_field': self._is_feedback_field(field),
            'expected_length': self._estimate_expected_length(field)
        }
        
        # Cache result
        self.field_cache[field_id] = analysis
        return analysis
    
    def analyze_form(self, form: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze entire form structure"""
        fields = form.get('fields', [])
        
        # Analyze each field
        field_analyses = []
        for field in fields:
            if not field.get('hide', False):
                field_analyses.append(self.analyze_field(field))
        
        # Detect relationships
        relationships = self._detect_field_relationships(fields)
        
        # Form-level analysis
        form_analysis = {
            'field_count': len(field_analyses),
            'required_count': sum(1 for f in field_analyses if f['is_required']),
            'feedback_fields': [f for f in field_analyses if f['is_feedback_field']],
            'rating_fields': [f for f in field_analyses if f['intent'] == FieldIntent.RATING],
            'personal_fields': [f for f in field_analyses if f['is_personal_data']],
            'field_analyses': field_analyses,
            'relationships': relationships,
            'form_type': self._detect_form_type(field_analyses),
            'estimated_completion_time': self._estimate_completion_time(field_analyses)
        }
        
        return form_analysis
    
    def _detect_intent(self, field: Dict[str, Any]) -> FieldIntent:
        """Detect the intent of a field based on its properties"""
        title = get_field_text(field.get('title')).lower()
        description = get_field_text(field.get('description')).lower()
        field_kind = field.get('kind', '')
        
        combined_text = f"{title} {description}"
        
        # Check each intent's keywords
        best_intent = FieldIntent.OTHER
        best_score = 0
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > best_score:
                best_score = score
                best_intent = intent
        
        # Override based on field type
        if field_kind == 'email':
            best_intent = FieldIntent.CONTACT
        elif field_kind == 'phone_number':
            best_intent = FieldIntent.CONTACT
        elif field_kind == 'rating' or field_kind == 'opinion_scale':
            best_intent = FieldIntent.RATING
        elif field_kind == 'address':
            best_intent = FieldIntent.LOCATION
        elif field_kind == 'date' or field_kind == 'time':
            best_intent = FieldIntent.TEMPORAL
        elif field_kind == 'legal':
            best_intent = FieldIntent.AGREEMENT
        
        return best_intent
    
    def _get_sentiment_category(self, field: Dict[str, Any]) -> FieldCategory:
        """Determine sentiment relevance of field"""
        field_kind = field.get('kind', '')
        intent = self._detect_intent(field)
        
        # First check by field type
        if field_kind in self.SENTIMENT_RELEVANCE:
            category = self.SENTIMENT_RELEVANCE[field_kind]
        else:
            category = FieldCategory.SENTIMENT_LOW
        
        # Override based on intent
        if intent == FieldIntent.FEEDBACK:
            category = FieldCategory.SENTIMENT_HIGH
        elif intent == FieldIntent.RATING:
            category = FieldCategory.SENTIMENT_HIGH
        elif intent in [FieldIntent.PERSONAL_INFO, FieldIntent.CONTACT, 
                        FieldIntent.DEMOGRAPHIC, FieldIntent.TEMPORAL]:
            category = FieldCategory.SENTIMENT_NONE
        
        return category
    
    def _extract_constraints(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Extract field constraints"""
        validations = field.get('validations', {})
        properties = field.get('properties', {})
        
        constraints = {
            'required': validations.get('required', False),
            'min_length': validations.get('minLength'),
            'max_length': validations.get('maxLength'),
            'min_value': validations.get('min'),
            'max_value': validations.get('max'),
            'pattern': validations.get('pattern'),
            'allow_multiple': properties.get('allowMultiple', False),
            'allow_other': properties.get('allowOther', False),
            'choice_count': len(properties.get('choices', []))
        }
        
        return {k: v for k, v in constraints.items() if v is not None}
    
    def _extract_keywords(self, field: Dict[str, Any]) -> List[str]:
        """Extract important keywords from field"""
        title = get_field_text(field.get('title'))
        description = get_field_text(field.get('description'))
        
        # Simple keyword extraction
        text = f"{title} {description}".lower()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 
                     'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is',
                     'are', 'was', 'were', 'been', 'be', 'have', 'has'}
        
        words = re.findall(r'\b\w+\b', text)
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return list(set(keywords))
    
    def _is_personal_data(self, field: Dict[str, Any]) -> bool:
        """Check if field contains personal data"""
        field_kind = field.get('kind', '')
        intent = self._detect_intent(field)
        
        personal_kinds = ['email', 'phone_number', 'full_name', 'address']
        personal_intents = [FieldIntent.PERSONAL_INFO, FieldIntent.CONTACT,
                           FieldIntent.DEMOGRAPHIC]
        
        return field_kind in personal_kinds or intent in personal_intents
    
    def _is_feedback_field(self, field: Dict[str, Any]) -> bool:
        """Check if field is for feedback/comments"""
        intent = self._detect_intent(field)
        field_kind = field.get('kind', '')
        title = get_field_text(field.get('title')).lower()
        
        return (intent == FieldIntent.FEEDBACK or 
                field_kind == 'long_text' or
                any(word in title for word in ['comment', 'feedback', 'suggestion']))
    
    def _estimate_expected_length(self, field: Dict[str, Any]) -> Tuple[int, int]:
        """Estimate expected response length"""
        field_kind = field.get('kind', '')
        validations = field.get('validations', {})
        
        min_length = validations.get('minLength', 0)
        max_length = validations.get('maxLength', 1000)
        
        # Adjust based on field type
        if field_kind == 'short_text':
            return (min_length or 5, min(max_length, 100))
        elif field_kind == 'long_text':
            return (min_length or 20, max_length)
        elif field_kind == 'email':
            return (5, 50)
        elif field_kind == 'phone_number':
            return (10, 20)
        else:
            return (min_length, max_length)
    
    def _detect_field_relationships(self, fields: List[Dict]) -> Dict[str, List[str]]:
        """Detect relationships between fields"""
        relationships = {}
        
        # Group fields by similar titles/types
        for i, field1 in enumerate(fields):
            if field1.get('hide'):
                continue
                
            field1_id = field1.get('id')
            related = []
            
            for j, field2 in enumerate(fields):
                if i == j or field2.get('hide'):
                    continue
                    
                field2_id = field2.get('id')
                
                # Check for related fields
                if self._are_fields_related(field1, field2):
                    related.append(field2_id)
            
            if related:
                relationships[field1_id] = related
        
        return relationships
    
    def _are_fields_related(self, field1: Dict, field2: Dict) -> bool:
        """Check if two fields are related"""
        # Similar titles
        title1 = get_field_text(field1.get('title', '')).lower()
        title2 = get_field_text(field2.get('title', '')).lower()
        
        # Check for common significant words
        words1 = set(re.findall(r'\b\w{4,}\b', title1))
        words2 = set(re.findall(r'\b\w{4,}\b', title2))
        
        if words1 & words2:
            return True
        
        # Same intent
        if self._detect_intent(field1) == self._detect_intent(field2):
            return True
        
        # Name fields (first/last)
        if ('first' in title1 and 'last' in title2) or ('first' in title2 and 'last' in title1):
            return True
        
        return False
    
    def _detect_form_type(self, field_analyses: List[Dict]) -> str:
        """Detect the type of form based on fields"""
        # Count field intents
        intent_counts = {}
        for analysis in field_analyses:
            intent = analysis['intent']
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        # Determine form type
        if intent_counts.get(FieldIntent.FEEDBACK, 0) >= 2:
            return 'feedback_survey'
        elif intent_counts.get(FieldIntent.RATING, 0) >= 3:
            return 'satisfaction_survey'
        elif intent_counts.get(FieldIntent.PERSONAL_INFO, 0) >= 3:
            return 'registration_form'
        elif intent_counts.get(FieldIntent.CONTACT, 0) >= 2:
            return 'contact_form'
        elif intent_counts.get(FieldIntent.PREFERENCE, 0) >= 3:
            return 'preference_survey'
        elif intent_counts.get(FieldIntent.DEMOGRAPHIC, 0) >= 2:
            return 'demographic_survey'
        else:
            return 'general_form'
    
    def _estimate_completion_time(self, field_analyses: List[Dict]) -> int:
        """Estimate form completion time in seconds"""
        base_time = 0
        
        for analysis in field_analyses:
            field_kind = analysis['kind']
            is_required = analysis['is_required']
            
            # Base time per field type
            if field_kind in ['short_text', 'email', 'phone_number']:
                base_time += 10
            elif field_kind in ['long_text']:
                base_time += 30
            elif field_kind in ['multiple_choice', 'dropdown']:
                base_time += 8
            elif field_kind in ['rating', 'yes_no']:
                base_time += 5
            elif field_kind in ['address', 'full_name']:
                base_time += 20
            elif field_kind in ['date', 'time']:
                base_time += 8
            elif field_kind in ['file_upload', 'signature']:
                base_time += 15
            else:
                base_time += 10
            
            # Add time for required fields (more consideration)
            if is_required:
                base_time += 2
        
        return base_time
    
    def get_field_priority(self, field_analysis: Dict) -> int:
        """Get priority score for field (higher = more important)"""
        priority = 0
        
        # Required fields have higher priority
        if field_analysis['is_required']:
            priority += 10
        
        # Feedback fields are important
        if field_analysis['is_feedback_field']:
            priority += 5
        
        # Rating fields are important
        if field_analysis['intent'] == FieldIntent.RATING:
            priority += 5
        
        # Personal data fields are medium priority
        if field_analysis['is_personal_data']:
            priority += 3
        
        return priority