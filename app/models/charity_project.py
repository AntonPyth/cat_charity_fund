from sqlalchemy import Column, String, Text

from app.models.donation_base import DonationsBase


class CharityProject(DonationsBase):
    """Модель благотворительного проекта.

    Атрибуты:
        name: Уникальное имя проекта (максимум 100 символов).
        description: Описание проекта.
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
