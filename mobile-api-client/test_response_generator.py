#!/usr/bin/env python3
"""Test script for the Response Generator"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from response_generator import ResponseGenerator, PersonaPool, Sentiment
from response_generator.personas import AgeGroup, Profession
from mobile_api_client import MobileAPIClient


def create_test_form():
    """Create a test form structure"""
    return {
        "id": "test-form-001",
        "name": "Customer Satisfaction Survey",
        "description": "Help us improve our service",
        "fields": [
            {
                "id": "name",
                "kind": "short_text",
                "title": "What's your full name?",
                "validations": {"required": True, "minLength": 2, "maxLength": 100}
            },
            {
                "id": "email",
                "kind": "email",
                "title": "Your email address",
                "validations": {"required": True}
            },
            {
                "id": "satisfaction",
                "kind": "multiple_choice",
                "title": "How satisfied are you with our service?",
                "validations": {"required": True},
                "properties": {
                    "choices": [
                        {"id": "very_satisfied", "label": "Very Satisfied", "score": 5},
                        {"id": "satisfied", "label": "Satisfied", "score": 4},
                        {"id": "neutral", "label": "Neutral", "score": 3},
                        {"id": "dissatisfied", "label": "Dissatisfied", "score": 2},
                        {"id": "very_dissatisfied", "label": "Very Dissatisfied", "score": 1}
                    ],
                    "allowMultiple": False,
                    "allowOther": True
                }
            },
            {
                "id": "rating",
                "kind": "rating",
                "title": "Rate our service quality",
                "validations": {"required": True},
                "properties": {"total": 10}
            },
            {
                "id": "recommend",
                "kind": "yes_no",
                "title": "Would you recommend us to others?",
                "validations": {"required": True}
            },
            {
                "id": "feedback",
                "kind": "long_text",
                "title": "Additional feedback",
                "description": "Please share any additional comments",
                "validations": {"required": False, "maxLength": 500}
            },
            {
                "id": "contact_date",
                "kind": "date",
                "title": "When did you last contact us?",
                "validations": {"required": False}
            },
            {
                "id": "phone",
                "kind": "phone_number",
                "title": "Phone number (optional)",
                "validations": {"required": False},
                "properties": {"defaultCountryCode": "+1"}
            }
        ]
    }


def test_single_response():
    """Test generating a single response"""
    print("\n" + "="*60)
    print("TEST 1: Single Response Generation")
    print("="*60)
    
    generator = ResponseGenerator(locale='en_US')
    form = create_test_form()
    
    # Test each sentiment
    for sentiment in ['positive', 'negative', 'neutral']:
        print(f"\n--- {sentiment.upper()} Sentiment ---")
        response = generator.generate_response(form, sentiment=sentiment)
        
        print(f"Generated {len(response)} field answers:")
        for field_id, value in response.items():
            print(f"  {field_id}: {value}")


def test_persona_based_generation():
    """Test generation with specific personas"""
    print("\n" + "="*60)
    print("TEST 2: Persona-Based Generation")
    print("="*60)
    
    generator = ResponseGenerator(locale='en_US')
    form = create_test_form()
    
    # Create specific personas
    from response_generator.personas import PersonaGenerator
    persona_gen = PersonaGenerator()
    
    # Young tech-savvy positive persona
    young_tech = persona_gen.generate(
        age_group=AgeGroup.YOUNG_ADULT,
        profession=Profession.TECH,
        sentiment=Sentiment.POSITIVE
    )
    
    print(f"\nPersona: {young_tech.first_name} {young_tech.last_name}")
    print(f"  Age: {young_tech.age}, Profession: {young_tech.job_title}")
    print(f"  Sentiment: {young_tech.base_sentiment.value}")
    print(f"  Tech Savvy: {young_tech.tech_savvy.value}")
    
    response = generator.generate_with_persona_story(form, young_tech)
    print("\nGenerated Response:")
    for field_id, value in response['answers'].items():
        print(f"  {field_id}: {value}")
    print(f"\nPersona Story: {response['persona_story']}")


def test_batch_generation():
    """Test batch generation with sentiment distribution"""
    print("\n" + "="*60)
    print("TEST 3: Batch Generation")
    print("="*60)
    
    generator = ResponseGenerator(locale='en_US')
    form = create_test_form()
    
    # Generate batch with specific sentiment distribution
    responses = generator.generate_batch(
        form=form,
        count=10,
        sentiment_distribution={
            'positive': 0.5,
            'neutral': 0.3,
            'negative': 0.2
        },
        variations=True
    )
    
    print(f"\nGenerated {len(responses)} responses")
    
    # Analyze sentiment distribution
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    partial_count = 0
    
    for resp in responses:
        sentiment = resp['metadata']['sentiment']
        sentiment_counts[sentiment] += 1
        if resp['metadata']['is_partial']:
            partial_count += 1
    
    print("\nSentiment Distribution:")
    for sentiment, count in sentiment_counts.items():
        print(f"  {sentiment}: {count} ({count/len(responses)*100:.1f}%)")
    print(f"\nPartial Submissions: {partial_count}")
    
    # Show sample response
    print("\nSample Response:")
    sample = responses[0]
    for field_id, value in sample['answers'].items():
        print(f"  {field_id}: {value}")


def test_persona_pool():
    """Test persona pool generation"""
    print("\n" + "="*60)
    print("TEST 4: Persona Pool")
    print("="*60)
    
    # Create diverse persona pool
    pool = PersonaPool(size=20, diversity='high', locale='en_US')
    
    stats = pool.get_statistics()
    print(f"\nPersona Pool Statistics:")
    print(f"  Total Personas: {stats['total']}")
    print(f"  Average Age: {stats['avg_age']:.1f}")
    
    print("\n  Age Groups:")
    for group, count in stats['age_groups'].items():
        print(f"    {group}: {count}")
    
    print("\n  Professions:")
    for prof, count in stats['professions'].items():
        print(f"    {prof}: {count}")
    
    print("\n  Sentiments:")
    for sent, count in stats['sentiments'].items():
        print(f"    {sent}: {count}")
    
    print("\n  Device Types:")
    for device, count in stats['device_types'].items():
        print(f"    {device}: {count}")


def test_field_analysis():
    """Test field analyzer"""
    print("\n" + "="*60)
    print("TEST 5: Field Analysis")
    print("="*60)
    
    from response_generator.field_analyzer import FieldAnalyzer
    
    analyzer = FieldAnalyzer()
    form = create_test_form()
    
    analysis = analyzer.analyze_form(form)
    
    print(f"\nForm Analysis:")
    print(f"  Form Type: {analysis['form_type']}")
    print(f"  Total Fields: {analysis['field_count']}")
    print(f"  Required Fields: {analysis['required_count']}")
    print(f"  Estimated Completion Time: {analysis['estimated_completion_time']}s")
    
    print("\nField Analysis:")
    for field_analysis in analysis['field_analyses']:
        print(f"\n  Field: {field_analysis['id']}")
        print(f"    Intent: {field_analysis['intent'].value}")
        print(f"    Sentiment Category: {field_analysis['sentiment_category'].value}")
        print(f"    Is Feedback: {field_analysis['is_feedback_field']}")
        print(f"    Is Personal Data: {field_analysis['is_personal_data']}")


def test_load_generation():
    """Test load test generation"""
    print("\n" + "="*60)
    print("TEST 6: Load Test Generation")
    print("="*60)
    
    generator = ResponseGenerator(locale='en_US')
    form = create_test_form()
    
    # Generate load test with 5 RPS for 10 seconds
    print("\nGenerating load test (5 RPS for 10 seconds)...")
    stats = generator.generate_load_test(
        form=form,
        responses_per_second=5,
        duration=10,
        sentiment_distribution={
            'positive': 0.6,
            'neutral': 0.3,
            'negative': 0.1
        },
        ramp_up_time=2,
        ramp_down_time=2
    )
    
    print(f"\nLoad Test Results:")
    print(f"  Target RPS: {stats['target_rps']}")
    print(f"  Actual RPS: {stats['actual_rps']:.2f}")
    print(f"  Total Responses: {stats['total_responses']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Partial: {stats['partial']}")
    print(f"  Avg Generation Time: {stats['avg_generation_time']:.3f}s")
    
    print("\n  Sentiment Distribution:")
    for sentiment, count in stats['sentiments'].items():
        if stats['successful'] > 0:
            percentage = count / stats['successful'] * 100
            print(f"    {sentiment}: {count} ({percentage:.1f}%)")


def test_export():
    """Test exporting responses"""
    print("\n" + "="*60)
    print("TEST 7: Export Responses")
    print("="*60)
    
    generator = ResponseGenerator(locale='en_US')
    form = create_test_form()
    
    # Generate some responses
    responses = generator.generate_batch(
        form=form,
        count=5,
        sentiment_distribution={'positive': 0.6, 'negative': 0.2, 'neutral': 0.2}
    )
    
    # Export to JSON
    generator.export_responses(responses, format='json', output_file='test_responses.json')
    print("✓ Exported to test_responses.json")
    
    # Export to CSV
    generator.export_responses(responses, format='csv', output_file='test_responses.csv')
    print("✓ Exported to test_responses.csv")


def test_with_real_api():
    """Test with real API client integration"""
    print("\n" + "="*60)
    print("TEST 8: Integration with API Client")
    print("="*60)
    
    generator = ResponseGenerator(locale='en_US')
    client = MobileAPIClient(base_url="http://localhost:9157", debug=False)
    
    # Try to fetch a real form (this will fail if no server is running)
    print("\nNote: This test requires a running server with an active form.")
    print("If no server is available, using test form instead.\n")
    
    form = create_test_form()  # Use test form as fallback
    
    # Generate responses
    print("Generating responses for form submission...")
    responses = generator.generate_batch(
        form=form,
        count=3,
        sentiment_distribution={'positive': 0.7, 'neutral': 0.2, 'negative': 0.1}
    )
    
    print(f"\nGenerated {len(responses)} responses ready for submission")
    
    # Validate responses
    try:
        for i, resp in enumerate(responses):
            validated = client.validate_answers(form, resp['answers'])
            print(f"  Response {i+1}: ✓ Valid ({len(validated)} fields)")
    except Exception as e:
        print(f"  Validation not available without API client setup: {e}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("RESPONSE GENERATOR TEST SUITE")
    print("="*60)
    
    tests = [
        test_single_response,
        test_persona_based_generation,
        test_batch_generation,
        test_persona_pool,
        test_field_analysis,
        test_load_generation,
        test_export,
        test_with_real_api
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\nTest failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Response Generator')
    parser.add_argument('--test', choices=[
        'single', 'persona', 'batch', 'pool', 'analysis', 
        'load', 'export', 'api', 'all'
    ], default='all', help='Test to run')
    
    args = parser.parse_args()
    
    if args.test == 'single':
        test_single_response()
    elif args.test == 'persona':
        test_persona_based_generation()
    elif args.test == 'batch':
        test_batch_generation()
    elif args.test == 'pool':
        test_persona_pool()
    elif args.test == 'analysis':
        test_field_analysis()
    elif args.test == 'load':
        test_load_generation()
    elif args.test == 'export':
        test_export()
    elif args.test == 'api':
        test_with_real_api()
    else:
        run_all_tests()