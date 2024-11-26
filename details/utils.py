from django.core.mail import send_mail
from django.conf import settings

def send_order_notification(to_email, subject, message):
    send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # From email address
            [to_email],  # Recipient email address
            fail_silently=False,  # Will raise an exception if email fails
    )
