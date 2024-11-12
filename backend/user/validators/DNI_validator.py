import re
from django.core.exceptions import ValidationError

def validate_dni(value):
    if not re.match(r'^\d{8}[A-Za-z]$', value):
        raise ValidationError(
            '%(value)s is not a valid DNI. It must be 8 digits followed by a letter.',
            params={'value': value},
        )