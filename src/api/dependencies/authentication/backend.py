from fastapi_users.authentication import AuthenticationBackend

from src.core.authentication.transport import bearer_transport

from .strategy import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="accesstokens",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)