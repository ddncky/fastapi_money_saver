import uvicorn
from sqladmin import Admin

from src.admin.auth import authentication_backend
from src.admin.models import AccountAdmin, CategoryAdmin, TransactionAdmin, UserAdmin
from src.core import get_database
from src.create_app import create_application

app = create_application()

admin = Admin(app, get_database().engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(AccountAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(TransactionAdmin)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
