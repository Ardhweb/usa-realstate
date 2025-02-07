from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
BLOCKED_TEMP_DOMAINS = {
    "tempmail.com", "10minutemail.com", "guerrillamail.com", "mailinator.com", 
    "fakeinbox.com", "yopmail.com", "throwawaymail.com", "maildrop.cc", "trashmail.com"
}

def checked_email_address(value):
    email_regex = r'^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$'
    match = re.match(email_regex, value)
    
    if match:
        domain = match.group(1)
        if domain in BLOCKED_TEMP_DOMAINS:
            raise ValidationError(_("Emails from temporary domains are not allowed."))
    else:
        raise ValidationError(_("Invalid email format"))



