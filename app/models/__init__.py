from .charity_project import CharityProject
from .donation import Donation

CharityProject.investment_counterpart = Donation
Donation.investment_counterpart = CharityProject
from .user import User


__all__ = [
    'CharityProject',
    'Donation',
    'User',
]
