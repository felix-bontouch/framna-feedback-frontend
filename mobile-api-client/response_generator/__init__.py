"""Response Generator Package for Automatic Form Response Generation"""

from .generator import ResponseGenerator
from .sentiment_engine import SentimentEngine, SentimentProfile, Sentiment
from .personas import PersonaPool, Persona, PersonaGenerator, AgeGroup, Profession
from .field_analyzer import FieldAnalyzer

__all__ = [
    'ResponseGenerator',
    'SentimentEngine',
    'SentimentProfile',
    'Sentiment',
    'PersonaPool',
    'Persona',
    'PersonaGenerator',
    'AgeGroup',
    'Profession',
    'FieldAnalyzer'
]

__version__ = '1.0.0'