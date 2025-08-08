#!/usr/bin/env python3
"""Command-line interface for Mobile API Client"""

import argparse
import json
import sys
from pathlib import Path
from mobile_api_client import MobileAPIClient
from exceptions import MobileAPIError


def cmd_get_form(args):
    """Get and display form structure"""
    client = MobileAPIClient(base_url=args.base_url, debug=args.debug)
    
    try:
        form = client.get_form(args.form_id)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(form, f, indent=2)
            print(f"Form saved to {args.output}")
        else:
            print(json.dumps(form, indent=2))
            
    except MobileAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_submit(args):
    """Submit form with answers from JSON file"""
    client = MobileAPIClient(base_url=args.base_url, debug=args.debug)
    
    try:
        # Load answers from file
        with open(args.answers, 'r') as f:
            data = json.load(f)
        
        # Extract answers and options
        if isinstance(data, dict) and 'answers' in data:
            answers = data['answers']
            password = data.get('password')
            captcha_token = data.get('captchaToken')
            category = data.get('category', 'GENERAL')
            hidden_fields = data.get('hiddenFields')
        else:
            answers = data
            password = args.password
            captcha_token = None
            category = 'GENERAL'
            hidden_fields = None
        
        # Fetch form for validation
        form = client.get_form(args.form_id)
        
        # Validate answers
        validated_answers = client.validate_answers(form, answers)
        
        # Submit
        result = client.submit_form(
            form_id=args.form_id,
            answers=validated_answers,
            password=password or args.password,
            captcha_token=captcha_token,
            category=category,
            hidden_fields=hidden_fields
        )
        
        print(f"Submission successful!")
        print(f"Submission ID: {result['submissionId']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {args.output}")
            
    except FileNotFoundError:
        print(f"Error: File not found: {args.answers}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.answers}: {e}", file=sys.stderr)
        sys.exit(1)
    except MobileAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_interactive(args):
    """Interactive form submission"""
    client = MobileAPIClient(base_url=args.base_url, debug=args.debug)
    
    try:
        result = client.interactive_submit(args.form_id, password=args.password)
        
        if result and args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {args.output}")
            
    except MobileAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_batch(args):
    """Batch submission from JSON file"""
    client = MobileAPIClient(base_url=args.base_url, debug=args.debug)
    
    try:
        # Load submissions from file
        with open(args.file, 'r') as f:
            data = json.load(f)
        
        # Extract submissions
        if isinstance(data, dict) and 'submissions' in data:
            submissions = data['submissions']
            form_id = data.get('form_id', args.form_id)
        else:
            submissions = data if isinstance(data, list) else [data]
            form_id = args.form_id
        
        if not form_id:
            print("Error: Form ID must be specified", file=sys.stderr)
            sys.exit(1)
        
        # Submit batch
        results = client.batch_submit(form_id, submissions, delay=args.delay)
        
        # Save results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        
        # Print summary
        successful = sum(1 for r in results if r['success'])
        print(f"\nBatch complete: {successful}/{len(results)} successful")
        
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.file}: {e}", file=sys.stderr)
        sys.exit(1)
    except MobileAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_validate(args):
    """Validate answers without submitting"""
    client = MobileAPIClient(base_url=args.base_url, debug=args.debug)
    
    try:
        # Load answers
        with open(args.answers, 'r') as f:
            data = json.load(f)
        
        answers = data.get('answers', data) if isinstance(data, dict) else data
        
        # Fetch form
        form = client.get_form(args.form_id)
        
        # Validate
        validated = client.validate_answers(form, answers)
        
        print("✓ Validation successful!")
        print("\nValidated answers:")
        print(json.dumps(validated, indent=2))
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(validated, f, indent=2)
            print(f"\nValidated answers saved to {args.output}")
            
    except FileNotFoundError:
        print(f"Error: File not found: {args.answers}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except MobileAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_fields(args):
    """Get specific fields from a form"""
    client = MobileAPIClient(base_url=args.base_url, debug=args.debug)
    
    try:
        field_ids = args.field_ids.split(',') if args.field_ids else None
        fields = client.get_fields(args.form_id, field_ids)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(fields, f, indent=2)
            print(f"Fields saved to {args.output}")
        else:
            print(json.dumps(fields, indent=2))
            
    except MobileAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Mobile API Client for Framna Feedback Forms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get form structure
  %(prog)s get-form test-form-123
  
  # Submit form with answers from JSON
  %(prog)s submit test-form-123 -a answers.json
  
  # Interactive submission
  %(prog)s interactive test-form-123
  
  # Batch submission
  %(prog)s batch -f submissions.json
  
  # Validate answers without submitting
  %(prog)s validate test-form-123 -a answers.json
        """
    )
    
    # Global arguments
    parser.add_argument('--base-url', '-u', 
                       default='http://localhost:9157',
                       help='API base URL (default: http://localhost:9157)')
    parser.add_argument('--debug', '-d', 
                       action='store_true',
                       help='Enable debug output')
    parser.add_argument('--output', '-o',
                       help='Output file for results')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    subparsers.required = True
    
    # get-form command
    parser_get = subparsers.add_parser('get-form', 
                                       help='Get form structure')
    parser_get.add_argument('form_id', help='Form ID')
    parser_get.set_defaults(func=cmd_get_form)
    
    # submit command
    parser_submit = subparsers.add_parser('submit', 
                                          help='Submit form with answers')
    parser_submit.add_argument('form_id', help='Form ID')
    parser_submit.add_argument('--answers', '-a', 
                               required=True,
                               help='JSON file with answers')
    parser_submit.add_argument('--password', '-p',
                               help='Form password if required')
    parser_submit.set_defaults(func=cmd_submit)
    
    # interactive command
    parser_interactive = subparsers.add_parser('interactive', 
                                               help='Interactive form submission')
    parser_interactive.add_argument('form_id', help='Form ID')
    parser_interactive.add_argument('--password', '-p',
                                    help='Form password if required')
    parser_interactive.set_defaults(func=cmd_interactive)
    
    # batch command
    parser_batch = subparsers.add_parser('batch', 
                                         help='Batch submission from JSON')
    parser_batch.add_argument('--form-id', '-f',
                             help='Form ID (can be in JSON file)')
    parser_batch.add_argument('--file', '-i',
                             required=True,
                             help='JSON file with submissions')
    parser_batch.add_argument('--delay',
                             type=float,
                             default=0.5,
                             help='Delay between submissions (default: 0.5s)')
    parser_batch.set_defaults(func=cmd_batch)
    
    # validate command
    parser_validate = subparsers.add_parser('validate', 
                                            help='Validate answers without submitting')
    parser_validate.add_argument('form_id', help='Form ID')
    parser_validate.add_argument('--answers', '-a',
                                 required=True,
                                 help='JSON file with answers')
    parser_validate.set_defaults(func=cmd_validate)
    
    # fields command
    parser_fields = subparsers.add_parser('fields', 
                                          help='Get specific fields from form')
    parser_fields.add_argument('form_id', help='Form ID')
    parser_fields.add_argument('--field-ids', '-f',
                               help='Comma-separated field IDs')
    parser_fields.set_defaults(func=cmd_fields)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    args.func(args)


if __name__ == '__main__':
    main()