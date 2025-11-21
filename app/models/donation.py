from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import declared_attr

from app.core.db import Base


class DonationsBase(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Donation(DonationsBase):
    investment_counterpart = None
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
