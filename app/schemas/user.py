from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Возвращается при чтении общедоступных данных пользователя.
    """


class UserCreate(schemas.BaseUserCreate):
    """
    Схема используется при создании нового пользователя.
    """


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема, используется для акцепта частичных обновлений пользовательских данных
    """
