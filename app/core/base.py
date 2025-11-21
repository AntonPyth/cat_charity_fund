"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base
from app.models import CharityProject, Donation, User

__all__ = [
    'Base',
    'CharityProject',
    'Donation',
    'User'
]
