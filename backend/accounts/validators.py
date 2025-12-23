import re
from django.core.exceptions import ValidationError


class PasswordComplexityValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                'Password must be at least 8 characters long.',
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                'Password must contain at least one uppercase letter.',
                code='password_no_upper',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                'Password must contain at least one number.',
                code='password_no_number',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                'Password must contain at least one special character.',
                code='password_no_special',
            )

    def get_help_text(self):
        return 'Password must be at least 8 characters long and contain at least one uppercase letter, one number, and one special character.'
