from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import AgeGroup

from core.mixins import SoftDeleteMixin, TimeStampedMixin

class UserProfile(TimeStampedMixin, SoftDeleteMixin, AbstractUser):
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True)
    is_public = models.BooleanField(
        default=True, help_text="Whether this profile is visible to other users"
    )
    dob = models.DateField(null=True, blank=True, help_text="Date of Birth")
    age_group = models.CharField(
        max_length=10, choices=AgeGroup.choices, blank=True, null=True
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username
