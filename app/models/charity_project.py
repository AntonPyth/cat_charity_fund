from sqlalchemy import Column, String, Text

from app.models.donation import DonationsBase


class CharityProject(DonationsBase):
    investment_counterpart = None
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
