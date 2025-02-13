from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

def validate_email_domain(value):
    """Custom email validator that allows only specific domains."""
    allowed_domains = ["example.com", "mycompany.com", "gmail.com", "outlook.com"]  # Allowed email domains

    if "@" not in value:
        raise ValidationError("Invalid email format.")

    email_domain = value.split("@")[-1]
    
    if email_domain not in allowed_domains:
        raise ValidationError(f"This email addres are not allowed.")
    
    # Optional regex validation (Example: Email must start with a letter)
    if not re.match(r"^[a-zA-Z][\w\.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$", value):
        raise ValidationError("Invalid email format.")


from django.core.exceptions import ValidationError
import re

class AlphanumericPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise ValidationError(
                "Password must contain at least one letter and one number.",
                code='password_no_alphanumeric',
            )

    def get_help_text(self):
        return "Your password must contain at least one letter and one number."
