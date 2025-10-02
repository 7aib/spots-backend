from django.db import models
from django.utils.translation import gettext_lazy as _


class AgeGroup(models.TextChoices):
    KID = "0-12", _("Kid (0-12)")
    TEEN = "13-19", _("Teen (13-19)")
    YOUNG_ADULT = "20-29", _("Young Adult (20-29)")
    ADULT = "30-44", _("Adult (30-44)")
    MIDDLE_AGED = "45-59", _("Middle-aged (45-59)")
    SENIOR = "60+", _("Senior (60+)")
