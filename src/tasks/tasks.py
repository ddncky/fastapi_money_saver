from .celery_client import celery
from src.core import get_settings
from .email_templates import create_registration_confirmation_template
import smtplib


@celery.task
def send_registration_confirmation_email(email_to):
    msg_content = create_registration_confirmation_template(email_to)

    with smtplib.SMTP_SSL(get_settings().SMTP_HOST, get_settings().SMTP_PORT) as server:
        server.login(get_settings().SMTP_USER, get_settings().SMTP_PASS)
        server.send_message(msg_content)
