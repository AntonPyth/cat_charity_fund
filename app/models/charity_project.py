from sqlalchemy import Column, String, Text

from app.models.donation import DonationsBase


class CharityProject(DonationsBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
