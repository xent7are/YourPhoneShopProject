import re
from datetime import datetime
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number

def validate_user_form(data):
    """
    Validates user form data.
    Args:
        data (dict): Form data with keys 'name', 'email', 'phone', 'birth_date'.
    Returns:
        list: List of error messages (empty if no errors).
    """
    errors = []

    # Check name (not empty)
    if not data.get('name', '').strip():
        errors.append("The 'Name' field is required.")

    # Check email (valid format)
    email = data.get('email', '').strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email:
        errors.append("The 'Email' field is required.")
    elif not re.match(email_pattern, email):
        errors.append("Email must be in the format example@domain.com.")

    # Check phone (valid international format using phonenumbers)
    phone = data.get('phone', '').strip()
    if not phone:
        errors.append("The 'Phone' field is required.")
    else:
        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not is_valid_number(parsed_phone):
                errors.append("Invalid phone number. Please enter a valid international phone number (e.g., +71234567890).")
        except NumberParseException:
            errors.append("Phone number format is invalid. Use international format (e.g., +71234567890).")

    # Check birth date (format YYYY-MM-DD)
    birth_date = data.get('birth_date', '').strip()
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not birth_date:
        errors.append("The 'Birth Date' field is required.")
    elif not re.match(date_pattern, birth_date):
        errors.append("Birth Date must be in the format YYYY-MM-DD (e.g., 2000-05-11).")
    else:
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
            # Optional: Check if birth date is not in the future
            if datetime.strptime(birth_date, '%Y-%m-%d') > datetime.now():
                errors.append("Birth Date cannot be in the future.")
        except ValueError:
            errors.append("Invalid Birth Date. Please check the entered values.")

    return errors