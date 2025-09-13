from django.db import models
from django.utils.translation import gettext_lazy as _

class AgeGroup(models.TextChoices):
    KID = '0-12', _('Kid (0-12)')
    TEEN = '13-19', _('Teen (13-19)')
    YOUNG_ADULT = '20-29', _('Young Adult (20-29)')
    ADULT = '30-44', _('Adult (30-44)')
    MIDDLE_AGED = '45-59', _('Middle-aged (45-59)')
    SENIOR = '60+', _('Senior (60+)')

class Provinces(models.TextChoices):
    PUNJAB = 'punjab', _('Punjab')
    SINDH = 'sindh', _('Sindh')
    KPK = 'kpk', _('Khyber Pakhtunkhwa')
    BALOCHISTAN = 'balochistan', _('Balochistan')
    GILGIT_BALTISTAN = 'gilgit_baltistan', _('Gilgit-Baltistan')
    ISLAMABAD = 'islamabad', _('Islamabad Capital Territory')
    AJK = 'ajk', _('Azad Jammu & Kashmir')