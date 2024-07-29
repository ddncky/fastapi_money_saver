from fastapi_users import FastAPIUsers

from src.api.dependencies.authentication.backend import authentication_backend
from src.api.dependencies.authentication.user_manager import get_user_manager
from src.modules import User

fastapi_users_inst = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users_inst.current_user(active=True)
current_active_superuser = fastapi_users_inst.current_user(active=True, superuser=True)