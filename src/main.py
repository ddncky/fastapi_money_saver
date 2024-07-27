from src.create_app import create_application
import uvicorn
from sqladmin import Admin
from src.core import get_database
from src.admin.models import UserAdmin, AccountAdmin, CategoryAdmin, TransactionAdmin
from src.admin.auth import authentication_backend


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
