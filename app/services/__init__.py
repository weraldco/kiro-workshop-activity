"""
Business logic services for workshop management.

This package contains service classes that implement business logic
for workshops, challenges, and registrations.
"""

from app.services.workshop_service import WorkshopService
from app.services.challenge_service import ChallengeService
from app.services.registration_service import RegistrationService

__all__ = [
    'WorkshopService',
    'ChallengeService',
    'RegistrationService',
]
