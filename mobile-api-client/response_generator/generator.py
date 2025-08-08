"""Main Response Generator for automatic form response generation"""

import random
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .sentiment_engine import SentimentEngine, Sentiment
from .personas import Persona, PersonaPool, PersonaGenerator
from .data_providers import DataProvider
from .field_generators import get_field_generator
from .field_analyzer import FieldAnalyzer


class ResponseGenerator:
    """Main class for generating form responses with sentiment control"""
    
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        """
        Initialize Response Generator
        
        Args:
            locale: Locale for data generation
            seed: Random seed for reproducibility
        """
        self.locale = locale
        self.sentiment_engine = SentimentEngine()
        self.data_provider = DataProvider(locale)
        self.field_analyzer = FieldAnalyzer()
        self.persona_generator = PersonaGenerator(locale)
        
        if seed:
            self.set_seed(seed)
    
    def set_seed(self, seed: int):
        """Set random seed for reproducibility"""
        random.seed(seed)
        self.data_provider.set_seed(seed)
    
    def generate_response(self, 
                         form: Dict[str, Any],
                         sentiment: str = 'neutral',
                         persona: Optional[Persona] = None,
                         partial_probability: float = 0.0) -> Dict[str, Any]:
        """
        Generate a single form response
        
        Args:
            form: Form structure dictionary
            sentiment: Sentiment type (positive, negative, neutral, mixed)
            persona: Optional persona to use
            partial_probability: Probability of partial submission (0-1)
        
        Returns:
            Dictionary of field answers
        """
        # Analyze form structure
        form_analysis = self.field_analyzer.analyze_form(form)
        
        # Create or use persona
        if not persona:
            # Generate persona with matching sentiment
            sentiment_enum = Sentiment(sentiment.lower()) if sentiment != 'mixed' else None
            persona = self.persona_generator.generate(sentiment=sentiment_enum)
        
        # Set sentiment
        if sentiment == 'mixed':
            # Random sentiment for mixed
            sentiment = random.choice(['positive', 'negative', 'neutral'])
        
        self.sentiment_engine.set_sentiment(sentiment)
        
        # Generate answers for each field
        answers = {}
        fields = form.get('fields', [])
        
        # Determine if this will be a partial submission
        is_partial = random.random() < partial_probability
        
        # Sort fields by priority if partial
        if is_partial:
            field_analyses = form_analysis['field_analyses']
            field_priority = [(fa, self.field_analyzer.get_field_priority(fa)) 
                            for fa in field_analyses]
            field_priority.sort(key=lambda x: x[1], reverse=True)
            
            # Only answer top 60-80% of fields
            num_to_answer = int(len(field_priority) * random.uniform(0.6, 0.8))
            fields_to_answer = set(fa['id'] for fa, _ in field_priority[:num_to_answer])
        else:
            fields_to_answer = None
        
        # Generate answers
        for field in fields:
            # Skip hidden fields
            if field.get('hide', False):
                continue
            
            field_id = field.get('id')
            
            # Skip if partial and not in fields to answer
            if is_partial and fields_to_answer and field_id not in fields_to_answer:
                continue
            
            # Skip non-required fields occasionally
            if not field.get('validations', {}).get('required', False):
                if random.random() < 0.1:  # Skip 10% of optional fields
                    continue
            
            # Generate value for field
            answer = self._generate_field_value(field, persona)
            if answer is not None:
                answers[field_id] = answer
        
        return answers
    
    def _generate_field_value(self, field: Dict[str, Any], 
                             persona: Persona) -> Any:
        """Generate value for a specific field"""
        field_kind = field.get('kind', 'short_text')
        
        # Get appropriate generator
        generator = get_field_generator(
            field_kind,
            self.sentiment_engine,
            self.data_provider,
            persona
        )
        
        # Generate value
        try:
            return generator.generate(field)
        except Exception as e:
            # Silently skip unsupported field types (like thank_you)
            field_kind = field.get('kind', '')
            if field_kind not in ['thank_you', 'statement', 'welcome']:
                print(f"Error generating value for field {field.get('id')}: {e}")
            return None
    
    def generate_batch(self,
                      form: Dict[str, Any],
                      count: int,
                      sentiment_distribution: Optional[Dict[str, float]] = None,
                      persona_pool: Optional[PersonaPool] = None,
                      variations: bool = True) -> List[Dict[str, Any]]:
        """
        Generate multiple form responses
        
        Args:
            form: Form structure dictionary
            count: Number of responses to generate
            sentiment_distribution: Distribution of sentiments
            persona_pool: Optional pool of personas to use
            variations: Whether to add variations (typos, partial, etc.)
        
        Returns:
            List of response dictionaries
        """
        if not sentiment_distribution:
            sentiment_distribution = {
                'positive': 0.4,
                'neutral': 0.4,
                'negative': 0.2
            }
        
        # Create persona pool if not provided
        if not persona_pool:
            diversity = 'high' if count > 50 else 'medium'
            persona_pool = PersonaPool(
                size=min(count, 100),
                diversity=diversity,
                locale=self.locale
            )
        
        # Get sentiment list
        sentiments = self.sentiment_engine.get_sentiment_distribution(
            count, sentiment_distribution
        )
        
        # Generate responses
        responses = []
        personas = persona_pool.get_batch(count)
        
        for i in range(count):
            sentiment = sentiments[i]
            persona = personas[i]
            
            # Determine partial probability
            partial_prob = 0.02 if variations else 0.0
            
            # Generate response
            response = self.generate_response(
                form=form,
                sentiment=sentiment,
                persona=persona,
                partial_probability=partial_prob
            )
            
            responses.append({
                'answers': response,
                'metadata': {
                    'persona_id': persona.persona_id,
                    'sentiment': sentiment,
                    'generated_at': datetime.now().isoformat(),
                    'is_partial': len(response) < len([f for f in form.get('fields', []) 
                                                      if not f.get('hide')])
                }
            })
        
        return responses
    
    def generate_load_test(self,
                          form: Dict[str, Any],
                          responses_per_second: float,
                          duration: int,
                          sentiment_distribution: Optional[Dict[str, float]] = None,
                          ramp_up_time: int = 0,
                          ramp_down_time: int = 0) -> Dict[str, Any]:
        """
        Generate responses for load testing
        
        Args:
            form: Form structure dictionary
            responses_per_second: Target RPS
            duration: Test duration in seconds
            sentiment_distribution: Distribution of sentiments
            ramp_up_time: Time to ramp up to target RPS
            ramp_down_time: Time to ramp down from target RPS
        
        Returns:
            Load test results and statistics
        """
        if not sentiment_distribution:
            sentiment_distribution = {
                'positive': 0.5,
                'neutral': 0.3,
                'negative': 0.2
            }
        
        # Calculate total responses
        total_responses = int(responses_per_second * duration)
        
        # Create large persona pool for variety
        persona_pool = PersonaPool(
            size=min(total_responses, 500),
            diversity='high',
            locale=self.locale
        )
        
        # Generate response schedule
        schedule = self._generate_load_schedule(
            responses_per_second,
            duration,
            ramp_up_time,
            ramp_down_time
        )
        
        # Statistics
        stats = {
            'total_responses': 0,
            'successful': 0,
            'failed': 0,
            'partial': 0,
            'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0},
            'avg_generation_time': 0,
            'responses': []
        }
        
        generation_times = []
        
        # Generate responses according to schedule
        for second, rps in enumerate(schedule):
            responses_this_second = int(rps)
            
            for _ in range(responses_this_second):
                start_time = time.time()
                
                try:
                    # Random sentiment
                    sentiment = random.choices(
                        list(sentiment_distribution.keys()),
                        weights=list(sentiment_distribution.values())
                    )[0]
                    
                    # Get random persona
                    persona = persona_pool.get_persona()
                    
                    # Generate response
                    response = self.generate_response(
                        form=form,
                        sentiment=sentiment,
                        persona=persona,
                        partial_probability=0.02
                    )
                    
                    generation_time = time.time() - start_time
                    generation_times.append(generation_time)
                    
                    # Update stats
                    stats['total_responses'] += 1
                    stats['successful'] += 1
                    stats['sentiments'][sentiment] += 1
                    
                    if len(response) < len([f for f in form.get('fields', []) 
                                           if not f.get('hide')]):
                        stats['partial'] += 1
                    
                    # Store response with metadata
                    stats['responses'].append({
                        'answers': response,
                        'timestamp': time.time(),
                        'second': second,
                        'generation_time': generation_time,
                        'sentiment': sentiment,
                        'persona_id': persona.persona_id
                    })
                    
                except Exception as e:
                    stats['failed'] += 1
                    print(f"Failed to generate response: {e}")
            
            # Small delay to simulate real-time generation
            if second < len(schedule) - 1:
                time.sleep(0.1)
        
        # Calculate average generation time
        if generation_times:
            stats['avg_generation_time'] = sum(generation_times) / len(generation_times)
        
        # Additional statistics
        stats['duration'] = duration
        stats['target_rps'] = responses_per_second
        stats['actual_rps'] = stats['total_responses'] / duration if duration > 0 else 0
        
        return stats
    
    def _generate_load_schedule(self,
                               target_rps: float,
                               duration: int,
                               ramp_up: int,
                               ramp_down: int) -> List[float]:
        """Generate RPS schedule for load test"""
        schedule = []
        
        # Ramp up phase
        for i in range(ramp_up):
            rps = target_rps * (i + 1) / ramp_up
            schedule.append(rps)
        
        # Steady state
        steady_duration = duration - ramp_up - ramp_down
        for _ in range(steady_duration):
            schedule.append(target_rps)
        
        # Ramp down phase
        for i in range(ramp_down):
            rps = target_rps * (ramp_down - i) / ramp_down
            schedule.append(rps)
        
        return schedule
    
    def generate_with_persona_story(self,
                                   form: Dict[str, Any],
                                   persona: Persona) -> Dict[str, Any]:
        """
        Generate response with consistent persona story
        
        Args:
            form: Form structure
            persona: Persona to use
        
        Returns:
            Response with persona's consistent story
        """
        # Set sentiment based on persona
        self.sentiment_engine.set_sentiment(
            persona.base_sentiment.value,
            intensity=persona.enthusiast_score if persona.base_sentiment == Sentiment.POSITIVE 
                     else persona.complainer_score
        )
        
        # Generate response
        response = self.generate_response(
            form=form,
            sentiment=persona.base_sentiment.value,
            persona=persona
        )
        
        # Add metadata about persona
        return {
            'answers': response,
            'persona_story': {
                'name': f"{persona.first_name} {persona.last_name}",
                'age': persona.age,
                'profession': persona.profession.value,
                'sentiment': persona.base_sentiment.value,
                'tech_savvy': persona.tech_savvy.value,
                'device': persona.device_type,
                'completion_time': persona.get_completion_time(len(response))
            }
        }
    
    def export_responses(self,
                        responses: List[Dict],
                        format: str = 'json',
                        output_file: str = 'responses.json') -> None:
        """
        Export generated responses to file
        
        Args:
            responses: List of response dictionaries
            format: Export format (json, csv)
            output_file: Output file path
        """
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(responses, f, indent=2, default=str)
        
        elif format == 'csv':
            import csv
            
            # Flatten responses for CSV
            if responses:
                # Get all field names
                field_names = set()
                for response in responses:
                    if 'answers' in response:
                        field_names.update(response['answers'].keys())
                
                field_names = sorted(list(field_names))
                
                with open(output_file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['_id'] + field_names + 
                                          ['_sentiment', '_persona_id', '_timestamp'])
                    writer.writeheader()
                    
                    for i, response in enumerate(responses):
                        row = {'_id': i}
                        
                        # Add answers
                        answers = response.get('answers', {})
                        for field in field_names:
                            value = answers.get(field, '')
                            # Simplify complex values for CSV
                            if isinstance(value, dict):
                                if 'value' in value:
                                    value = ','.join(value['value']) if isinstance(value['value'], list) else value['value']
                                else:
                                    value = json.dumps(value)
                            elif isinstance(value, list):
                                value = json.dumps(value)
                            row[field] = value
                        
                        # Add metadata
                        metadata = response.get('metadata', {})
                        row['_sentiment'] = metadata.get('sentiment', '')
                        row['_persona_id'] = metadata.get('persona_id', '')
                        row['_timestamp'] = metadata.get('generated_at', '')
                        
                        writer.writerow(row)
        
        print(f"Exported {len(responses)} responses to {output_file}")