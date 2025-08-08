#!/usr/bin/env python3
"""CLI for Response Generator - Automatic form response generation with sentiment control"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from response_generator import ResponseGenerator, PersonaPool
from mobile_api_client import MobileAPIClient


def cmd_generate(args):
    """Generate single response"""
    # Load form
    if args.form_file:
        with open(args.form_file, 'r') as f:
            form = json.load(f)
    elif args.form_id:
        # Fetch from API
        client = MobileAPIClient(base_url=args.api_url)
        form = client.get_form(args.form_id)
    else:
        print("Error: Either --form-file or --form-id required")
        sys.exit(1)
    
    # Generate response
    generator = ResponseGenerator(locale=args.locale, seed=args.seed)
    response = generator.generate_response(
        form=form,
        sentiment=args.sentiment,
        partial_probability=args.partial_prob
    )
    
    # Output
    output = {
        'answers': response,
        'metadata': {
            'sentiment': args.sentiment,
            'locale': args.locale
        }
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Response saved to {args.output}")
    else:
        print(json.dumps(output, indent=2))


def cmd_batch(args):
    """Generate batch of responses"""
    # Load form
    if args.form_file:
        with open(args.form_file, 'r') as f:
            form = json.load(f)
    elif args.form_id:
        client = MobileAPIClient(base_url=args.api_url)
        form = client.get_form(args.form_id)
    else:
        print("Error: Either --form-file or --form-id required")
        sys.exit(1)
    
    # Parse sentiment distribution
    sentiment_dist = {}
    if args.sentiment_dist:
        for part in args.sentiment_dist.split(','):
            sentiment, weight = part.split(':')
            sentiment_dist[sentiment] = float(weight)
    else:
        sentiment_dist = {
            'positive': 0.4,
            'neutral': 0.4,
            'negative': 0.2
        }
    
    # Generate batch
    generator = ResponseGenerator(locale=args.locale, seed=args.seed)
    responses = generator.generate_batch(
        form=form,
        count=args.count,
        sentiment_distribution=sentiment_dist,
        variations=args.variations
    )
    
    # Export
    generator.export_responses(
        responses,
        format=args.format,
        output_file=args.output or f'batch_{args.count}.{args.format}'
    )
    
    # Print summary
    print(f"\nGenerated {len(responses)} responses")
    sentiment_counts = {}
    for resp in responses:
        sent = resp['metadata']['sentiment']
        sentiment_counts[sent] = sentiment_counts.get(sent, 0) + 1
    
    print("\nSentiment Distribution:")
    for sent, count in sentiment_counts.items():
        print(f"  {sent}: {count} ({count/len(responses)*100:.1f}%)")


def cmd_load_test(args):
    """Generate load test"""
    # Load form
    if args.form_file:
        with open(args.form_file, 'r') as f:
            form = json.load(f)
    elif args.form_id:
        client = MobileAPIClient(base_url=args.api_url)
        form = client.get_form(args.form_id)
    else:
        print("Error: Either --form-file or --form-id required")
        sys.exit(1)
    
    # Parse sentiment distribution
    sentiment_dist = {}
    if args.sentiment_dist:
        for part in args.sentiment_dist.split(','):
            sentiment, weight = part.split(':')
            sentiment_dist[sentiment] = float(weight)
    else:
        sentiment_dist = None
    
    # Run load test
    generator = ResponseGenerator(locale=args.locale, seed=args.seed)
    print(f"\nRunning load test: {args.rps} RPS for {args.duration}s")
    print("Press Ctrl+C to stop\n")
    
    try:
        stats = generator.generate_load_test(
            form=form,
            responses_per_second=args.rps,
            duration=args.duration,
            sentiment_distribution=sentiment_dist,
            ramp_up_time=args.ramp_up,
            ramp_down_time=args.ramp_down
        )
        
        # Print results
        print(f"\n{'='*60}")
        print("LOAD TEST RESULTS")
        print('='*60)
        print(f"Target RPS: {stats['target_rps']}")
        print(f"Actual RPS: {stats['actual_rps']:.2f}")
        print(f"Total Responses: {stats['total_responses']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print(f"Partial: {stats['partial']}")
        print(f"Avg Generation Time: {stats['avg_generation_time']:.3f}s")
        
        print("\nSentiment Distribution:")
        for sentiment, count in stats['sentiments'].items():
            if stats['successful'] > 0:
                percentage = count / stats['successful'] * 100
                print(f"  {sentiment}: {count} ({percentage:.1f}%)")
        
        # Export responses if requested
        if args.output:
            generator.export_responses(
                stats['responses'],
                format='json',
                output_file=args.output
            )
            print(f"\nResponses saved to {args.output}")
            
    except KeyboardInterrupt:
        print("\nLoad test interrupted")


def cmd_submit(args):
    """Generate and submit responses to API"""
    # Initialize clients
    client = MobileAPIClient(base_url=args.api_url, debug=args.debug)
    generator = ResponseGenerator(locale=args.locale, seed=args.seed)
    
    # Get form
    form = client.get_form(args.form_id)
    print(f"Form: {form['name']}")
    print(f"Fields: {len(form.get('fields', []))}")
    
    # Parse sentiment distribution
    sentiment_dist = {}
    if args.sentiment_dist:
        for part in args.sentiment_dist.split(','):
            sentiment, weight = part.split(':')
            sentiment_dist[sentiment] = float(weight)
    else:
        sentiment_dist = {
            'positive': 0.6,
            'neutral': 0.3,
            'negative': 0.1
        }
    
    # Generate responses
    print(f"\nGenerating {args.count} responses...")
    responses = generator.generate_batch(
        form=form,
        count=args.count,
        sentiment_distribution=sentiment_dist
    )
    
    # Submit responses
    print(f"Submitting responses...")
    successful = 0
    failed = 0
    
    for i, resp in enumerate(responses, 1):
        try:
            # Validate
            validated = client.validate_answers(form, resp['answers'])
            
            # Submit
            result = client.submit_form(args.form_id, validated)
            successful += 1
            print(f"  {i}/{args.count}: ✓ {result['submissionId']}")
            
            # Delay between submissions
            if args.delay > 0 and i < len(responses):
                import time
                time.sleep(args.delay)
                
        except Exception as e:
            failed += 1
            print(f"  {i}/{args.count}: ✗ {e}")
    
    print(f"\nSubmission complete: {successful} successful, {failed} failed")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Response Generator - Automatic form response generation with sentiment control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single response
  %(prog)s generate --form-file form.json --sentiment positive
  
  # Generate batch of 100 responses
  %(prog)s batch --form-id abc123 --count 100 --sentiment-dist positive:0.6,neutral:0.3,negative:0.1
  
  # Run load test
  %(prog)s load-test --form-file form.json --rps 10 --duration 60
  
  # Generate and submit to API
  %(prog)s submit --form-id abc123 --count 50 --api-url http://localhost:9157
        """
    )
    
    # Global arguments
    parser.add_argument('--api-url', default='http://localhost:9157',
                       help='API base URL')
    parser.add_argument('--locale', default='en_US',
                       help='Locale for data generation')
    parser.add_argument('--seed', type=int,
                       help='Random seed for reproducibility')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug output')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    subparsers.required = True
    
    # Generate command
    parser_gen = subparsers.add_parser('generate', help='Generate single response')
    parser_gen.add_argument('--form-file', help='Form JSON file')
    parser_gen.add_argument('--form-id', help='Form ID to fetch from API')
    parser_gen.add_argument('--sentiment', default='neutral',
                           choices=['positive', 'negative', 'neutral', 'mixed'],
                           help='Sentiment type')
    parser_gen.add_argument('--partial-prob', type=float, default=0.0,
                           help='Probability of partial submission (0-1)')
    parser_gen.add_argument('--output', '-o', help='Output file')
    parser_gen.set_defaults(func=cmd_generate)
    
    # Batch command
    parser_batch = subparsers.add_parser('batch', help='Generate batch of responses')
    parser_batch.add_argument('--form-file', help='Form JSON file')
    parser_batch.add_argument('--form-id', help='Form ID to fetch from API')
    parser_batch.add_argument('--count', type=int, default=10,
                             help='Number of responses to generate')
    parser_batch.add_argument('--sentiment-dist',
                             help='Sentiment distribution (e.g., positive:0.6,neutral:0.3,negative:0.1)')
    parser_batch.add_argument('--variations', action='store_true',
                             help='Add variations (typos, partial, etc.)')
    parser_batch.add_argument('--format', choices=['json', 'csv'], default='json',
                             help='Export format')
    parser_batch.add_argument('--output', '-o', help='Output file')
    parser_batch.set_defaults(func=cmd_batch)
    
    # Load test command
    parser_load = subparsers.add_parser('load-test', help='Generate load test')
    parser_load.add_argument('--form-file', help='Form JSON file')
    parser_load.add_argument('--form-id', help='Form ID to fetch from API')
    parser_load.add_argument('--rps', type=float, default=5,
                            help='Responses per second')
    parser_load.add_argument('--duration', type=int, default=60,
                            help='Test duration in seconds')
    parser_load.add_argument('--ramp-up', type=int, default=0,
                            help='Ramp up time in seconds')
    parser_load.add_argument('--ramp-down', type=int, default=0,
                            help='Ramp down time in seconds')
    parser_load.add_argument('--sentiment-dist',
                            help='Sentiment distribution')
    parser_load.add_argument('--output', '-o', help='Save responses to file')
    parser_load.set_defaults(func=cmd_load_test)
    
    # Submit command
    parser_submit = subparsers.add_parser('submit', 
                                          help='Generate and submit to API')
    parser_submit.add_argument('form_id', help='Form ID')
    parser_submit.add_argument('--count', type=int, default=10,
                              help='Number of responses')
    parser_submit.add_argument('--sentiment-dist',
                              help='Sentiment distribution')
    parser_submit.add_argument('--delay', type=float, default=0.5,
                              help='Delay between submissions')
    parser_submit.set_defaults(func=cmd_submit)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()