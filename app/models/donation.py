from sqlalchemy import Column, ForeignKey, Integer, Text

from .donation_base import DonationsBase


class Donation(DonationsBase):
    """Модель пожертвования, вклад пользователя в благотворительный проект.

    Атрибуты:
        user_id:    ссылка на внешний ключ пользователя,
                    который сделал пожертвование.
        comment:    Необязательный текстовый комментарий,
                    предоставленный донором.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
