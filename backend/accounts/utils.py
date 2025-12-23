import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailVerificationToken, PasswordResetToken


def generate_token():
    return secrets.token_urlsafe(32)


def create_email_verification_token(user):
    token_string = generate_token()
    token = EmailVerificationToken.objects.create(user=user, token=token_string)
    return token


def create_password_reset_token(user):
    token_string = generate_token()
    token = PasswordResetToken.objects.create(user=user, token=token_string)
    return token


def send_verification_email(user, token):
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token.token}"
    
    subject = 'Verify your email address'
    html_message = render_to_string('emails/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER or 'noreply@sme-finance.com',
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, token):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token.token}"
    
    subject = 'Reset your password'
    html_message = render_to_string('emails/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER or 'noreply@sme-finance.com',
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
