from django.db import models
from django.utils.translation import gettext_lazy as _


class Provinces(models.TextChoices):
    PUNJAB = "punjab", _("Punjab")
    SINDH = "sindh", _("Sindh")
    KPK = "kpk", _("Khyber Pakhtunkhwa")
    BALOCHISTAN = "balochistan", _("Balochistan")
    GILGIT_BALTISTAN = "gilgit_baltistan", _("Gilgit-Baltistan")
    ISLAMABAD = "islamabad", _("Islamabad Capital Territory")
    AJK = "ajk", _("Azad Jammu & Kashmir")
