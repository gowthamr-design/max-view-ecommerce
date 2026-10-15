import secrets
import string
import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

logger = logging.getLogger(__name__)


def generate_otp(length=6) -> str:
    """Generate a secure, random numeric OTP."""
    digits = string.digits
    return ''.join(secrets.choice(digits) for _ in range(length))


def create_email_otp(email: str, purpose: str, session_data: dict = None) -> EmailOTP:
    """
    Generate an OTP and save it to the database with expiration timestamp.
    Invalidate any previous unverified OTPs for the same email and purpose.
    """
    EmailOTP.objects.filter(email=email, purpose=purpose, is_verified=False).delete()

    otp_code = generate_otp(6)
    expiry_minutes = getattr(settings, 'EMAIL_OTP_EXPIRY_MINUTES', 10)
    expires_at = timezone.now() + timedelta(minutes=expiry_minutes)

    otp_obj = EmailOTP.objects.create(
        email=email,
        otp_code=otp_code,
        purpose=purpose,
        session_data=session_data or {},
        expires_at=expires_at,
    )
    return otp_obj


def send_otp_email(email: str, otp_code: str, purpose: str, user_name: str = None) -> bool:
    """
    Send OTP verification email via configured SMTP backend.
    Returns True if sent successfully, False otherwise.
    """
    name_greeting = f"Hello {user_name}," if user_name else "Hello,"
    expiry_minutes = getattr(settings, 'EMAIL_OTP_EXPIRY_MINUTES', 10)

    if purpose == EmailOTP.PURPOSE_REGISTRATION:
        subject = f"{otp_code} is your MAX VIEW account verification code"
        message = (
            f"{name_greeting}\n\n"
            f"Thank you for registering with MAX VIEW.\n\n"
            f"Your one-time verification code is:\n\n"
            f"    {otp_code}\n\n"
            f"This code will expire in {expiry_minutes} minutes.\n"
            f"If you did not request this code, please ignore this email.\n\n"
            f"Regards,\n"
            f"MAX VIEW Luxury Fashion Team\n"
            f"123@ Tirupur, Tamil Nadu, INDIA"
        )
    elif purpose == EmailOTP.PURPOSE_PASSWORD_RESET:
        subject = f"{otp_code} is your MAX VIEW password reset code"
        message = (
            f"{name_greeting}\n\n"
            f"We received a request to reset your MAX VIEW account password.\n\n"
            f"Your one-time password reset code is:\n\n"
            f"    {otp_code}\n\n"
            f"This code will expire in {expiry_minutes} minutes.\n"
            f"If you did not request a password reset, you can safely ignore this email.\n\n"
            f"Regards,\n"
            f"MAX VIEW Security Concierge\n"
            f"123@ Tirupur, Tamil Nadu, INDIA"
        )
    else:
        subject = f"Your MAX VIEW verification code: {otp_code}"
        message = (
            f"{name_greeting}\n\n"
            f"Your verification code is: {otp_code}\n"
            f"Valid for {expiry_minutes} minutes.\n\n"
            f"MAX VIEW Luxury Fashion"
        )

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'MAX VIEW <noreply@maxview.com>')

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"OTP email sent successfully to {email} for {purpose}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send OTP email to {email}: {exc}")
        return False
