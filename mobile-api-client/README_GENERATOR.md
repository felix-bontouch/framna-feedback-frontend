# Response Generator for Framna Feedback Forms

An intelligent, sentiment-aware automatic response generator for testing forms with realistic data. Generate thousands of responses with configurable sentiment distributions, realistic personas, and dynamic field handling.

## Features

### 🎭 Sentiment-Aware Generation
- **Positive**: Enthusiastic, satisfied responses with high ratings
- **Negative**: Critical, dissatisfied responses with low ratings  
- **Neutral**: Balanced, factual responses with moderate ratings
- **Mixed**: Realistic distribution across all sentiments

### 👥 Persona System
- **Diverse Demographics**: Age groups, professions, locations
- **Consistent Profiles**: Each persona maintains consistent characteristics
- **Behavioral Traits**: Typing speed, error rates, response styles
- **Device Simulation**: Mobile, desktop, tablet patterns

### 🔄 Dynamic Field Handling
- **20+ Field Types**: All Framna field types supported
- **Intelligent Analysis**: Understands field intent and context
- **Validation-Aware**: Respects all field constraints
- **Relationship Detection**: Maintains consistency across related fields

### 📊 Load Testing
- **Configurable RPS**: Set target responses per second
- **Ramp Up/Down**: Gradual load increase/decrease
- **Real-time Statistics**: Track generation performance
- **Export Results**: Save for analysis

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For response generator specific deps
pip install faker nltk numpy pyyaml pandas
```

## Quick Start

### 1. Generate Single Response

```python
from response_generator import ResponseGenerator

generator = ResponseGenerator()
response = generator.generate_response(
    form=form_dict,
    sentiment='positive'
)
```

### 2. Generate Batch with Sentiment Distribution

```python
responses = generator.generate_batch(
    form=form_dict,
    count=100,
    sentiment_distribution={
        'positive': 0.6,
        'neutral': 0.3,
        'negative': 0.1
    }
)
```

### 3. Use CLI for Quick Generation

```bash
# Generate single positive response
python response_gen_cli.py generate --form-file form.json --sentiment positive

# Generate batch of 100 responses
python response_gen_cli.py batch --form-id abc123 --count 100 \
    --sentiment-dist positive:0.6,neutral:0.3,negative:0.1

# Run load test
python response_gen_cli.py load-test --form-file form.json \
    --rps 10 --duration 60

# Generate and submit to API
python response_gen_cli.py submit form-id --count 50 \
    --api-url http://localhost:9157
```

## Sentiment Profiles

### Positive Sentiment
- **Ratings**: 80% score 8-10
- **Choices**: Selects positive options (Very Satisfied, Excellent)
- **Text**: Enthusiastic language with compliments
- **Recommendations**: 85% would recommend
- **Length**: Tends to write more when happy

### Negative Sentiment  
- **Ratings**: 75% score 1-4
- **Choices**: Selects negative options (Dissatisfied, Poor)
- **Text**: Critical language with complaints
- **Recommendations**: 10% would recommend
- **Length**: Detailed problem descriptions

### Neutral Sentiment
- **Ratings**: 60% score 4-6
- **Choices**: Middle-ground options (Neutral, Average)
- **Text**: Factual, balanced language
- **Recommendations**: 45% would recommend
- **Length**: Standard response length

## Persona System

### Creating Custom Personas

```python
from response_generator import PersonaGenerator, AgeGroup, Profession, Sentiment

generator = PersonaGenerator()

# Young tech professional with positive sentiment
persona = generator.generate(
    age_group=AgeGroup.YOUNG_ADULT,
    profession=Profession.TECH,
    sentiment=Sentiment.POSITIVE
)

# Use persona for consistent responses
response = response_generator.generate_response(
    form=form,
    persona=persona
)
```

### Persona Pools

```python
from response_generator import PersonaPool

# Create diverse pool
pool = PersonaPool(
    size=100,
    diversity='high',  # high, medium, low
    locale='en_US'
)

# Get statistics
stats = pool.get_statistics()
print(f"Age groups: {stats['age_groups']}")
print(f"Professions: {stats['professions']}")
print(f"Sentiments: {stats['sentiments']}")
```

## Field Intelligence

The generator analyzes fields to understand their purpose:

```python
from response_generator import FieldAnalyzer

analyzer = FieldAnalyzer()
analysis = analyzer.analyze_form(form)

print(f"Form type: {analysis['form_type']}")
print(f"Feedback fields: {len(analysis['feedback_fields'])}")
print(f"Rating fields: {len(analysis['rating_fields'])}")
print(f"Estimated completion time: {analysis['estimated_completion_time']}s")
```

### Field Intent Detection
- **Personal Info**: Names, demographics
- **Contact**: Email, phone, address
- **Feedback**: Comments, suggestions
- **Rating**: Satisfaction, quality scores
- **Preference**: Choices, selections
- **Temporal**: Dates, times, schedules

## Load Testing

### Basic Load Test

```python
stats = generator.generate_load_test(
    form=form,
    responses_per_second=10,
    duration=300,  # 5 minutes
    sentiment_distribution={
        'positive': 0.6,
        'neutral': 0.3,
        'negative': 0.1
    }
)

print(f"Generated: {stats['total_responses']}")
print(f"Actual RPS: {stats['actual_rps']:.2f}")
print(f"Avg generation time: {stats['avg_generation_time']:.3f}s")
```

### Advanced Load Pattern

```python
# Ramp up over 30s, steady for 5min, ramp down over 30s
stats = generator.generate_load_test(
    form=form,
    responses_per_second=50,
    duration=360,
    ramp_up_time=30,
    ramp_down_time=30
)
```

## Configuration

### Set Random Seed for Reproducibility

```python
generator = ResponseGenerator(seed=42)
```

### Locale Support

```python
# Generate with different locales
generator_us = ResponseGenerator(locale='en_US')
generator_uk = ResponseGenerator(locale='en_GB')
generator_es = ResponseGenerator(locale='es_ES')
```

### Export Formats

```python
# Export to JSON
generator.export_responses(responses, format='json', output_file='responses.json')

# Export to CSV
generator.export_responses(responses, format='csv', output_file='responses.csv')
```

## Advanced Features

### Partial Submissions

```python
# 10% chance of partial submission
response = generator.generate_response(
    form=form,
    partial_probability=0.1
)
```

### Typos and Errors

```python
# Personas with low tech savvy make more typos
persona = generator.generate(
    tech_savvy=TechSavvy.LOW  # Higher error rate
)
```

### Field Relationships

The generator maintains consistency across related fields:
- First/Last name consistency
- Email matches name
- Address components align
- Dates in logical order

## Examples

### Example 1: Customer Satisfaction Survey

```python
# Generate realistic customer feedback
responses = generator.generate_batch(
    form=satisfaction_form,
    count=1000,
    sentiment_distribution={
        'positive': 0.60,  # 60% happy customers
        'neutral': 0.30,   # 30% neutral
        'negative': 0.10   # 10% unhappy
    }
)
```

### Example 2: Registration Form Testing

```python
# Generate diverse user registrations
pool = PersonaPool(size=500, diversity='high')
responses = []

for persona in pool:
    response = generator.generate_response(
        form=registration_form,
        persona=persona
    )
    responses.append(response)
```

### Example 3: A/B Testing

```python
# Generate responses for A/B test variants
variant_a_responses = generator.generate_batch(
    form=form_variant_a,
    count=500,
    sentiment_distribution={'positive': 0.5, 'neutral': 0.5}
)

variant_b_responses = generator.generate_batch(
    form=form_variant_b,
    count=500,
    sentiment_distribution={'positive': 0.5, 'neutral': 0.5}
)
```

## API Integration

### With Mobile API Client

```python
from mobile_api_client import MobileAPIClient
from response_generator import ResponseGenerator

client = MobileAPIClient(base_url="http://localhost:9157")
generator = ResponseGenerator()

# Fetch form
form = client.get_form("form-id")

# Generate responses
responses = generator.generate_batch(form, count=100)

# Submit to API
for response in responses:
    validated = client.validate_answers(form, response['answers'])
    result = client.submit_form("form-id", validated)
```

## Performance

- **Generation Speed**: ~0.01-0.05s per response
- **Memory Efficient**: Streaming generation for large batches
- **Concurrent Safe**: Thread-safe for parallel generation
- **Scalable**: Handle thousands of responses

## Best Practices

1. **Use Personas for Consistency**: Create persona pools for realistic variation
2. **Match Real Distribution**: Use actual user sentiment ratios
3. **Test Edge Cases**: Include partial submissions and errors
4. **Validate Before Submission**: Always validate generated responses
5. **Set Seeds for Reproducibility**: Use seeds for consistent test data

## Troubleshooting

### Common Issues

**Issue**: Responses failing validation
**Solution**: Check field constraints and ensure generator respects them

**Issue**: Unrealistic sentiment distribution
**Solution**: Adjust sentiment weights based on actual user data

**Issue**: Slow generation for large batches
**Solution**: Use smaller persona pools, disable variations

## License

MIT

## Support

For issues or questions, please contact the development team.