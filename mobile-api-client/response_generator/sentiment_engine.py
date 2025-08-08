"""Sentiment Engine for generating sentiment-aware responses"""

import random
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum


class Sentiment(Enum):
    """Sentiment types"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class SentimentProfile:
    """Profile for a specific sentiment with associated patterns and phrases"""
    
    def __init__(self, sentiment: Sentiment):
        self.sentiment = sentiment
        self.phrases = self._load_phrases()
        self.patterns = self._load_patterns()
        self.intensity_range = self._get_intensity_range()
    
    def _load_phrases(self) -> Dict[str, List[str]]:
        """Load sentiment-specific phrases"""
        if self.sentiment == Sentiment.POSITIVE:
            return {
                'opening': [
                    'I absolutely love',
                    'Really impressed with',
                    'Fantastic experience with',
                    'Very happy with',
                    'Exceeded my expectations',
                    'Delighted by',
                    'Thoroughly enjoyed',
                    'Couldn\'t be happier with'
                ],
                'middle': [
                    'particularly enjoyed',
                    'was especially pleased with',
                    'really appreciated',
                    'found it excellent',
                    'works perfectly',
                    'exactly what I needed',
                    'outstanding quality',
                    'exceptional service'
                ],
                'closing': [
                    'Keep up the great work!',
                    'Highly recommend!',
                    'Will definitely return!',
                    'Can\'t wait to come back!',
                    'Thank you so much!',
                    'Absolutely perfect!',
                    '10/10 would recommend!',
                    'Best experience ever!'
                ],
                'adjectives': [
                    'amazing', 'excellent', 'outstanding', 'fantastic',
                    'wonderful', 'brilliant', 'superb', 'great',
                    'perfect', 'exceptional', 'impressive', 'delightful'
                ]
            }
        elif self.sentiment == Sentiment.NEGATIVE:
            return {
                'opening': [
                    'Very disappointed with',
                    'Not satisfied with',
                    'Expected much better from',
                    'Had issues with',
                    'Frustrated by',
                    'Not happy about',
                    'Concerned about',
                    'Problems with'
                ],
                'middle': [
                    'particularly poor',
                    'needs improvement',
                    'was unacceptable',
                    'didn\'t work properly',
                    'failed to deliver',
                    'below expectations',
                    'very problematic',
                    'seriously lacking'
                ],
                'closing': [
                    'Needs significant improvement.',
                    'Will look for alternatives.',
                    'Cannot recommend.',
                    'Very disappointing.',
                    'Please address these issues.',
                    'Won\'t be returning.',
                    'Expected better.',
                    'Not worth it.'
                ],
                'adjectives': [
                    'poor', 'terrible', 'awful', 'bad',
                    'disappointing', 'unacceptable', 'problematic', 'inferior',
                    'substandard', 'inadequate', 'unsatisfactory', 'frustrating'
                ]
            }
        else:  # NEUTRAL
            return {
                'opening': [
                    'My experience was',
                    'I found it to be',
                    'The service was',
                    'Overall, it was',
                    'In general,',
                    'From my perspective,',
                    'I would describe it as',
                    'It was'
                ],
                'middle': [
                    'acceptable',
                    'as expected',
                    'standard',
                    'adequate',
                    'satisfactory',
                    'reasonable',
                    'fair',
                    'average'
                ],
                'closing': [
                    'Thank you.',
                    'No major issues.',
                    'Met basic expectations.',
                    'Adequate overall.',
                    'Nothing special to note.',
                    'Standard experience.',
                    'As expected.',
                    'Fair enough.'
                ],
                'adjectives': [
                    'okay', 'fine', 'adequate', 'acceptable',
                    'average', 'standard', 'typical', 'regular',
                    'normal', 'satisfactory', 'decent', 'fair'
                ]
            }
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Load response patterns for this sentiment"""
        if self.sentiment == Sentiment.POSITIVE:
            return {
                'rating_distribution': {
                    'low': (1, 3, 0.05),    # min, max, probability
                    'medium': (4, 6, 0.15),
                    'high': (7, 8, 0.30),
                    'very_high': (9, 10, 0.50)
                },
                'yes_no_probability': 0.90,
                'recommendation_probability': 0.85,
                'text_length_factor': 1.2,  # Tend to write more when happy
                'use_exclamation': 0.4,
                'use_emoji': 0.15
            }
        elif self.sentiment == Sentiment.NEGATIVE:
            return {
                'rating_distribution': {
                    'very_low': (1, 2, 0.40),
                    'low': (3, 4, 0.35),
                    'medium': (5, 6, 0.20),
                    'high': (7, 10, 0.05)
                },
                'yes_no_probability': 0.15,
                'recommendation_probability': 0.10,
                'text_length_factor': 1.3,  # Tend to explain problems in detail
                'use_exclamation': 0.2,
                'use_emoji': 0.02
            }
        else:  # NEUTRAL
            return {
                'rating_distribution': {
                    'low': (1, 3, 0.15),
                    'medium': (4, 6, 0.60),
                    'high': (7, 8, 0.20),
                    'very_high': (9, 10, 0.05)
                },
                'yes_no_probability': 0.50,
                'recommendation_probability': 0.45,
                'text_length_factor': 1.0,
                'use_exclamation': 0.05,
                'use_emoji': 0.0
            }
    
    def _get_intensity_range(self) -> Tuple[float, float]:
        """Get intensity range for this sentiment"""
        if self.sentiment == Sentiment.POSITIVE:
            return (0.6, 1.0)
        elif self.sentiment == Sentiment.NEGATIVE:
            return (0.0, 0.4)
        else:
            return (0.4, 0.6)
    
    def get_phrase(self, category: str) -> str:
        """Get a random phrase from a category"""
        if category in self.phrases:
            return random.choice(self.phrases[category])
        return ""
    
    def get_rating(self, min_val: int = 1, max_val: int = 10) -> int:
        """Generate a rating based on sentiment distribution"""
        dist = self.patterns['rating_distribution']
        
        # Calculate probabilities
        rand = random.random()
        cumulative = 0
        
        for key, (range_min, range_max, prob) in dist.items():
            cumulative += prob
            if rand <= cumulative:
                # Scale to the actual min/max
                scaled_min = int((range_min - 1) / 9 * (max_val - min_val) + min_val)
                scaled_max = int((range_max - 1) / 9 * (max_val - min_val) + min_val)
                return random.randint(scaled_min, scaled_max)
        
        # Fallback
        return random.randint(min_val, max_val)
    
    def get_boolean(self, context: str = 'general') -> bool:
        """Generate a boolean value based on sentiment"""
        if context == 'recommendation':
            prob = self.patterns['recommendation_probability']
        else:
            prob = self.patterns['yes_no_probability']
        
        return random.random() < prob


class SentimentEngine:
    """Main sentiment engine for generating sentiment-aware content"""
    
    def __init__(self):
        self.profiles = {
            Sentiment.POSITIVE: SentimentProfile(Sentiment.POSITIVE),
            Sentiment.NEGATIVE: SentimentProfile(Sentiment.NEGATIVE),
            Sentiment.NEUTRAL: SentimentProfile(Sentiment.NEUTRAL)
        }
        self.current_sentiment = Sentiment.NEUTRAL
        self.intensity = 0.5
    
    def set_sentiment(self, sentiment: str, intensity: float = None):
        """Set the current sentiment"""
        try:
            self.current_sentiment = Sentiment(sentiment.lower())
        except ValueError:
            self.current_sentiment = Sentiment.NEUTRAL
        
        if intensity is not None:
            self.intensity = max(0.0, min(1.0, intensity))
        else:
            # Set default intensity based on sentiment
            profile = self.profiles[self.current_sentiment]
            min_int, max_int = profile.intensity_range
            self.intensity = random.uniform(min_int, max_int)
    
    def get_profile(self) -> SentimentProfile:
        """Get the current sentiment profile"""
        return self.profiles[self.current_sentiment]
    
    def generate_text(self, field_title: str, min_length: int = 10, 
                     max_length: int = 500) -> str:
        """Generate sentiment-aware text for a field"""
        profile = self.get_profile()
        
        # Determine text length based on sentiment
        base_length = random.randint(min_length, min(max_length, 200))
        length = int(base_length * profile.patterns['text_length_factor'])
        length = max(min_length, min(length, max_length))
        
        # Build the text
        parts = []
        
        # Opening
        if random.random() < 0.7:
            opening = profile.get_phrase('opening')
            if opening:
                parts.append(f"{opening} {field_title.lower()}.")
        
        # Middle content
        if length > 50:
            middle_phrases = []
            num_middle = min(3, length // 50)
            for _ in range(num_middle):
                middle = profile.get_phrase('middle')
                if middle:
                    adjective = random.choice(profile.phrases['adjectives'])
                    middle_phrases.append(f"The {field_title.lower()} was {middle}.")
            
            if middle_phrases:
                parts.extend(middle_phrases)
        
        # Add some generic content if needed
        if len(' '.join(parts)) < length // 2:
            generic = self._generate_generic_content(field_title, profile)
            parts.append(generic)
        
        # Closing
        if random.random() < 0.6:
            closing = profile.get_phrase('closing')
            if closing:
                parts.append(closing)
        
        # Join and format
        text = ' '.join(parts)
        
        # Add punctuation variations
        if profile.patterns['use_exclamation'] > random.random():
            text = text.replace('.', '!', 1)
        
        # Ensure within length limits
        if len(text) > max_length:
            text = text[:max_length-3] + '...'
        elif len(text) < min_length:
            # Pad with generic content
            padding = self._generate_generic_content(field_title, profile)
            text = f"{text} {padding}"[:max_length]
        
        return text.strip()
    
    def _generate_generic_content(self, field_title: str, profile: SentimentProfile) -> str:
        """Generate generic content based on sentiment"""
        templates = {
            Sentiment.POSITIVE: [
                f"Everything about {field_title.lower()} exceeded expectations.",
                "The quality was remarkable.",
                "I'm very impressed with the attention to detail.",
                "This is exactly what I was looking for."
            ],
            Sentiment.NEGATIVE: [
                f"The {field_title.lower()} needs serious improvement.",
                "Many aspects were below standard.",
                "I encountered several issues that need addressing.",
                "This did not meet my basic expectations."
            ],
            Sentiment.NEUTRAL: [
                f"The {field_title.lower()} was as described.",
                "It met the basic requirements.",
                "There were both positives and negatives.",
                "Overall, it was an average experience."
            ]
        }
        
        return random.choice(templates.get(profile.sentiment, ["No additional comments."]))
    
    def generate_choice_selection(self, choices: List[Dict], 
                                 allow_multiple: bool = False,
                                 allow_other: bool = False) -> Dict:
        """Generate choice selection based on sentiment"""
        profile = self.get_profile()
        
        # Analyze choices for sentiment alignment
        scored_choices = []
        for choice in choices:
            label = choice.get('label', '').lower()
            score = choice.get('score', 0)
            
            # Calculate sentiment alignment
            if self.current_sentiment == Sentiment.POSITIVE:
                if any(word in label for word in ['excellent', 'great', 'very satisfied', 'love', 'best']):
                    alignment = 1.0
                elif any(word in label for word in ['good', 'satisfied', 'happy', 'yes']):
                    alignment = 0.7
                elif any(word in label for word in ['neutral', 'okay', 'average']):
                    alignment = 0.3
                else:
                    alignment = 0.1
            elif self.current_sentiment == Sentiment.NEGATIVE:
                if any(word in label for word in ['poor', 'terrible', 'very dissatisfied', 'worst']):
                    alignment = 1.0
                elif any(word in label for word in ['bad', 'dissatisfied', 'unhappy', 'no']):
                    alignment = 0.7
                elif any(word in label for word in ['neutral', 'okay', 'average']):
                    alignment = 0.3
                else:
                    alignment = 0.1
            else:  # NEUTRAL
                if any(word in label for word in ['neutral', 'okay', 'average', 'adequate']):
                    alignment = 1.0
                else:
                    alignment = 0.5
            
            # Adjust by score if available
            if score > 0:
                if self.current_sentiment == Sentiment.POSITIVE:
                    alignment *= (score / 5.0)
                elif self.current_sentiment == Sentiment.NEGATIVE:
                    alignment *= ((6 - score) / 5.0)
            
            scored_choices.append((choice, alignment))
        
        # Sort by alignment
        scored_choices.sort(key=lambda x: x[1], reverse=True)
        
        # Select choices
        if allow_multiple:
            # Select 1-3 choices based on alignment
            num_choices = random.randint(1, min(3, len(choices)))
            selected = []
            for choice, alignment in scored_choices[:num_choices]:
                if alignment > 0.5 or random.random() < 0.3:
                    selected.append(choice['id'])
            
            if not selected and scored_choices:
                selected = [scored_choices[0][0]['id']]
            
            return {"value": selected}
        else:
            # Select single best choice
            if scored_choices:
                # Add some randomness
                if random.random() < 0.8:
                    selected = scored_choices[0][0]['id']
                else:
                    # Sometimes pick second best
                    idx = min(1, len(scored_choices) - 1)
                    selected = scored_choices[idx][0]['id']
                
                # Occasionally use "other" for negative sentiment
                if allow_other and self.current_sentiment == Sentiment.NEGATIVE and random.random() < 0.2:
                    return {
                        "value": [],
                        "other": profile.get_phrase('middle')
                    }
                
                return {"value": [selected]}
            
            return {"value": []}
    
    def get_sentiment_distribution(self, count: int, 
                                  distribution: Dict[str, float] = None) -> List[str]:
        """Generate a list of sentiments based on distribution"""
        if distribution is None:
            distribution = {
                'positive': 0.4,
                'neutral': 0.4,
                'negative': 0.2
            }
        
        sentiments = []
        for sentiment, ratio in distribution.items():
            sentiments.extend([sentiment] * int(count * ratio))
        
        # Fill remaining with weighted random
        while len(sentiments) < count:
            rand = random.random()
            cumulative = 0
            for sentiment, ratio in distribution.items():
                cumulative += ratio
                if rand <= cumulative:
                    sentiments.append(sentiment)
                    break
        
        # Shuffle for randomness
        random.shuffle(sentiments)
        return sentiments[:count]