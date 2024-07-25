import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin
from src.core import get_settings

from src.modules import User
from src.tasks.tasks import send_registration_confirmation_email

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from fastapi import Request


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = get_settings().reset_password_token_secret
    verification_token_secret = get_settings().verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        log.warning("User %r has registered.", user.id)
        send_registration_confirmation_email.delay(user.email)

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional["Request"] = None
    ):
        log.warning("User %r has forgot their password. Reset token: %r", user.id, token)

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional["Request"] = None
    ):
        log.warning(f"Verification requested for user %r. Verification token: %r", user.id, token)


