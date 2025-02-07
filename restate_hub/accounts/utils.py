from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
def send_email_sfa(subject, recipient_email,otp,url):
    subject = subject
    from_email=settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    custom_msg = ''
    # Context for the template
    context = {
        'otp':otp,
        'custom_msg':custom_msg,
        'url':url,
    }
    # Render the HTML template
    html_content = render_to_string('utils/email_otp.html', context)
    text_content = strip_tags(html_content)  # Fallback for plain text email
    
    # Create the email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        recipient_list
    )
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    email.send()
