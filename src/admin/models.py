from sqladmin import ModelView

from src.modules import Account, Category, Transaction, User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    can_delete = False
    can_edit = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [User.hashed_password]


class AccountAdmin(ModelView, model=Account):
    column_list = "__all__"
    name = "Счет"
    name_plural = "Счета"
    icon = "fa-solid fa-wallet"


class CategoryAdmin(ModelView, model=Category):
    column_list = "__all__"
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-list-ol"


class TransactionAdmin(ModelView, model=Transaction):
    column_list = "__all__"
    name = "Транзакция"
    name_plural = "Транзакции"
    icon = "fa-solid fa-dollar-sign"
