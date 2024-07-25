from email.message import EmailMessage

from pydantic import EmailStr

from src.core import get_settings


def create_registration_confirmation_template(
        email_to: EmailStr
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = get_settings().SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Подтвердите бронирование!</h1>
        Пользователь {email_to} был успешно зарегестрирован!
        """,
        subtype="html"
    )

    return email



