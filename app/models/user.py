from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    модель пользователя, которая комбинирует
    собственную ORM-модель (Base)
    с базовым шаблоном пользователя из FastAPI Users
    """
