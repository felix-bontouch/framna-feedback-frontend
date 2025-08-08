"""Mobile API Client for Framna Feedback Forms"""

import time
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from exceptions import (
    FormNotFoundError,
    FormInactiveError,
    ValidationError,
    QuotaExceededError,
    RateLimitError,
    PasswordRequiredError,
    CaptchaRequiredError,
    MobileAPIError
)
from field_handlers import format_answer, parse_field_input
from validators import validate_field
from utils import (
    build_client_info,
    generate_timestamp,
    pretty_print_json
)


class MobileAPIClient:
    """Client for interacting with Framna Feedback Mobile API"""
    
    def __init__(self,
                 base_url: str = "http://localhost:9157",
                 timeout: int = 30,
                 retry_attempts: int = 3,
                 verify_ssl: bool = True,
                 debug: bool = False,
                 cache_forms: bool = True,
                 cache_ttl: int = 300):
        """
        Initialize Mobile API Client
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts for failed requests
            verify_ssl: Whether to verify SSL certificates
            debug: Enable debug mode with verbose output
            cache_forms: Whether to cache form structures
            cache_ttl: Cache time-to-live in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.debug = debug
        self.cache_forms = cache_forms
        self.cache_ttl = cache_ttl
        
        # Form cache
        self._form_cache = {}
        self._cache_timestamps = {}
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=retry_attempts,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _debug_log(self, message: str, data: Any = None):
        """Log debug message if debug mode is enabled"""
        if self.debug:
            print(f"[DEBUG] {message}")
            if data:
                pretty_print_json(data)
    
    def _is_cache_valid(self, form_id: str) -> bool:
        """Check if cached form is still valid"""
        if not self.cache_forms:
            return False
        
        if form_id not in self._form_cache:
            return False
        
        cache_time = self._cache_timestamps.get(form_id, 0)
        return (time.time() - cache_time) < self.cache_ttl
    
    def _handle_error_response(self, response: requests.Response, form_id: str = None):
        """Handle API error responses"""
        try:
            error_data = response.json()
        except (ValueError, requests.exceptions.JSONDecodeError):
            error_data = {"message": response.text or f"HTTP {response.status_code}"}
        
        self._debug_log(f"Error response: {response.status_code}", error_data)
        
        # Handle specific error codes
        if response.status_code == 404:
            raise FormNotFoundError(form_id or "unknown")
        
        elif response.status_code == 400:
            message = error_data.get('message', 'Bad Request')
            
            # Check for specific error conditions
            if 'not active' in message.lower():
                raise FormInactiveError(form_id or "unknown", message)
            elif 'suspended' in message.lower():
                raise FormInactiveError(form_id or "unknown", message)
            elif 'quota exceeded' in message.lower():
                raise QuotaExceededError(form_id or "unknown")
            elif 'password' in message.lower():
                raise PasswordRequiredError(form_id or "unknown")
            elif 'captcha' in message.lower():
                raise CaptchaRequiredError(form_id or "unknown", 
                                         error_data.get('captchaKind', 'unknown'))
            elif 'field' in error_data:
                # Field validation error
                raise ValidationError(
                    message=message,
                    field_id=error_data.get('field'),
                    field_title=error_data.get('fieldTitle'),
                    field_kind=error_data.get('fieldKind'),
                    value=error_data.get('value')
                )
            else:
                raise MobileAPIError(message)
        
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            raise RateLimitError(int(retry_after) if retry_after else None)
        
        else:
            raise MobileAPIError(f"API request failed: {error_data.get('message', response.text)}")
    
    def get_form(self, form_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fetch form structure from API
        
        Args:
            form_id: The ID of the form to fetch
            force_refresh: Force refresh even if cached
        
        Returns:
            Form structure dictionary
        """
        # Check cache
        if not force_refresh and self._is_cache_valid(form_id):
            self._debug_log(f"Using cached form: {form_id}")
            return self._form_cache[form_id]
        
        url = f"{self.base_url}/api/mobile/forms/{form_id}"
        self._debug_log(f"Fetching form: {url}")
        
        try:
            response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
            
            if response.status_code != 200:
                self._handle_error_response(response, form_id)
            
            form_data = response.json()
            
            # Cache the form
            if self.cache_forms:
                self._form_cache[form_id] = form_data
                self._cache_timestamps[form_id] = time.time()
            
            self._debug_log(f"Successfully fetched form with {len(form_data.get('fields', []))} fields")
            return form_data
            
        except requests.RequestException as e:
            raise MobileAPIError(f"Failed to fetch form: {e}")
    
    def get_fields(self, form_id: str, field_ids: List[str] = None) -> Dict[str, Any]:
        """
        Get specific fields from a form
        
        Args:
            form_id: The ID of the form
            field_ids: List of field IDs to retrieve (None for all)
        
        Returns:
            Dictionary containing the requested fields
        """
        url = f"{self.base_url}/api/mobile/forms/{form_id}/fields"
        params = {}
        
        if field_ids:
            params['fieldIds'] = ','.join(field_ids)
        
        self._debug_log(f"Fetching fields: {url}", params)
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout, 
                                      verify=self.verify_ssl)
            
            if response.status_code != 200:
                self._handle_error_response(response, form_id)
            
            return response.json()
            
        except requests.RequestException as e:
            raise MobileAPIError(f"Failed to fetch fields: {e}")
    
    def submit_form(self,
                   form_id: str,
                   answers: Dict[str, Any],
                   client_info: Optional[Dict[str, Any]] = None,
                   category: str = "GENERAL",
                   password: Optional[str] = None,
                   captcha_token: Optional[str] = None,
                   hidden_fields: Optional[List[Dict]] = None,
                   is_partial: bool = False) -> Dict[str, Any]:
        """
        Submit form answers to the API
        
        Args:
            form_id: The ID of the form to submit
            answers: Dictionary of field_id -> answer value
            client_info: Optional client information override
            category: Submission category (NPS, FEATURE, USER_FLOW, etc.)
            password: Form password if required
            captcha_token: Captcha verification token if required
            hidden_fields: List of hidden field values
            is_partial: Whether this is a partial submission
        
        Returns:
            Submission response dictionary
        """
        # Build submission data
        submission_data = {
            "answers": answers,
            "startedAt": generate_timestamp(),
            "clientInfo": build_client_info(client_info),
            "category": category,
            "isPartial": is_partial
        }
        
        if password:
            submission_data["password"] = password
        
        if captcha_token:
            submission_data["captchaToken"] = captcha_token
        
        if hidden_fields:
            submission_data["hiddenFields"] = hidden_fields
        
        url = f"{self.base_url}/api/mobile/forms/{form_id}"
        self._debug_log(f"Submitting form: {url}", submission_data)
        
        try:
            response = self.session.post(
                url,
                json=submission_data,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            if response.status_code not in (200, 201):
                self._handle_error_response(response, form_id)
            
            result = response.json()
            self._debug_log("Submission successful", result)
            return result
            
        except requests.RequestException as e:
            raise MobileAPIError(f"Failed to submit form: {e}")
    
    def validate_answers(self, form: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate answers against form fields before submission
        
        Args:
            form: Form structure dictionary
            answers: Dictionary of field_id -> answer value
        
        Returns:
            Validated and formatted answers
        
        Raises:
            ValidationError: If validation fails
        """
        validated_answers = {}
        
        # Create field lookup
        field_map = {}
        for field in form.get('fields', []):
            field_map[field['id']] = field
            # Handle nested fields in groups
            if field.get('properties', {}).get('fields'):
                for nested_field in field['properties']['fields']:
                    field_map[nested_field['id']] = nested_field
        
        # Validate each answer
        for field_id, value in answers.items():
            if field_id not in field_map:
                self._debug_log(f"Warning: Field {field_id} not found in form")
                continue
            
            field = field_map[field_id]
            
            # Skip hidden fields
            if field.get('hide'):
                continue
            
            try:
                # Validate and format the answer
                validated_value = validate_field(field, value)
                formatted_value = format_answer(field, validated_value)
                validated_answers[field_id] = formatted_value
            except ValidationError as e:
                self._debug_log(f"Validation error for field {field_id}: {e}")
                raise
        
        # Check for required fields that are missing
        for field in form.get('fields', []):
            if field.get('hide'):
                continue
            
            if field.get('validations', {}).get('required'):
                if field['id'] not in validated_answers:
                    raise ValidationError(
                        "This field is required",
                        field_id=field['id'],
                        field_title=field.get('title'),
                        field_kind=field['kind']
                    )
        
        return validated_answers
    
    def build_answers_from_input(self, form: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build properly formatted answers from user input
        
        Args:
            form: Form structure dictionary
            input_data: Dictionary of field_id/field_title -> user input
        
        Returns:
            Formatted answers ready for submission
        """
        answers = {}
        
        # Create field lookup by ID and title
        field_map = {}
        for field in form.get('fields', []):
            field_map[field['id']] = field
            if field.get('title'):
                field_map[field['title']] = field
        
        # Process input data
        for key, value in input_data.items():
            field = field_map.get(key)
            if not field:
                self._debug_log(f"Warning: Field '{key}' not found")
                continue
            
            try:
                # Parse input based on field type
                if isinstance(value, str):
                    parsed_value = parse_field_input(field, value)
                else:
                    parsed_value = value
                
                # Validate and format
                validated_value = validate_field(field, parsed_value)
                formatted_value = format_answer(field, validated_value)
                answers[field['id']] = formatted_value
                
            except (ValidationError, ValueError) as e:
                self._debug_log(f"Error processing field '{key}': {e}")
                raise ValidationError(
                    str(e),
                    field_id=field['id'],
                    field_title=field.get('title'),
                    field_kind=field['kind'],
                    value=value
                )
        
        return answers
    
    def interactive_submit(self, form_id: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Interactive form submission with user prompts
        
        Args:
            form_id: The ID of the form to submit
            password: Form password if required
        
        Returns:
            Submission response
        """
        # Fetch form
        form = self.get_form(form_id)
        print(f"\nForm: {form['name']}")
        if form.get('description'):
            print(f"Description: {form['description']}")
        print(f"Fields: {len(form.get('fields', []))}\n")
        
        answers = {}
        
        # Iterate through fields
        for field in form.get('fields', []):
            if field.get('hide'):
                continue
            
            # Display field info
            print(f"\n{field.get('title', field['id'])} ({field['kind']})")
            if field.get('description'):
                print(f"  {field['description']}")
            
            # Show validation requirements
            validations = field.get('validations', {})
            if validations.get('required'):
                print("  * Required")
            if validations.get('minLength'):
                print(f"  * Min length: {validations['minLength']}")
            if validations.get('maxLength'):
                print(f"  * Max length: {validations['maxLength']}")
            
            # Show choices for choice fields
            if field['kind'] in ('multiple_choice', 'dropdown'):
                properties = field.get('properties', {})
                choices = properties.get('choices', [])
                if choices:
                    print("  Choices:")
                    for i, choice in enumerate(choices, 1):
                        print(f"    {i}. {choice['label']}")
                if properties.get('allowOther'):
                    print("    (or type 'other:' followed by custom text)")
                if properties.get('allowMultiple'):
                    print("    (multiple selections allowed, separate with comma)")
            
            # Get user input
            while True:
                try:
                    user_input = input("  > ").strip()
                    
                    # Skip if not required and empty
                    if not user_input and not validations.get('required'):
                        break
                    
                    # Parse and validate input
                    parsed_value = parse_field_input(field, user_input)
                    validated_value = validate_field(field, parsed_value)
                    formatted_value = format_answer(field, validated_value)
                    answers[field['id']] = formatted_value
                    break
                    
                except (ValidationError, ValueError) as e:
                    print(f"  Error: {e}")
                    print("  Please try again.")
        
        # Confirm submission
        print("\n" + "="*50)
        print("Ready to submit the form.")
        confirm = input("Submit? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Submission cancelled.")
            return None
        
        # Submit form
        try:
            result = self.submit_form(form_id, answers, password=password)
            print(f"\nSuccess! Submission ID: {result['submissionId']}")
            return result
        except MobileAPIError as e:
            print(f"\nSubmission failed: {e}")
            raise
    
    def batch_submit(self, form_id: str, submissions: List[Dict[str, Any]], 
                    delay: float = 0.5) -> List[Dict[str, Any]]:
        """
        Submit multiple form responses in batch
        
        Args:
            form_id: The ID of the form
            submissions: List of submission dictionaries with answers
            delay: Delay between submissions in seconds
        
        Returns:
            List of submission results
        """
        # Fetch form once for validation
        form = self.get_form(form_id)
        results = []
        
        print(f"Batch submitting {len(submissions)} responses to form {form_id}")
        
        for i, submission in enumerate(submissions, 1):
            print(f"Processing submission {i}/{len(submissions)}...")
            
            try:
                # Extract submission parameters
                answers = submission.get('answers', {})
                client_info = submission.get('clientInfo')
                category = submission.get('category', 'GENERAL')
                password = submission.get('password')
                captcha_token = submission.get('captchaToken')
                hidden_fields = submission.get('hiddenFields')
                
                # Validate answers
                validated_answers = self.validate_answers(form, answers)
                
                # Submit
                result = self.submit_form(
                    form_id=form_id,
                    answers=validated_answers,
                    client_info=client_info,
                    category=category,
                    password=password,
                    captcha_token=captcha_token,
                    hidden_fields=hidden_fields
                )
                
                results.append({
                    'index': i,
                    'success': True,
                    'result': result
                })
                
                print(f"  ✓ Submission {i} successful: {result['submissionId']}")
                
            except MobileAPIError as e:
                results.append({
                    'index': i,
                    'success': False,
                    'error': str(e)
                })
                print(f"  ✗ Submission {i} failed: {e}")
            
            # Delay between submissions
            if i < len(submissions) and delay > 0:
                time.sleep(delay)
        
        # Summary
        successful = sum(1 for r in results if r['success'])
        print(f"\nBatch complete: {successful}/{len(submissions)} successful")
        
        return results