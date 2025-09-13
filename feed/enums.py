from django.db import models

class MEDIA_TYPES(models.TextChoices):
    """Media types"""
    PHOTO = 'photo', 'Photo'
    VIDEO = 'video', 'Video'
