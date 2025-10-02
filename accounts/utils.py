from datetime import date
from .choices import AgeGroup


def get_age_group(self, dob):
        if not dob:
            return None
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age <= 12:
            return AgeGroup.KID
        elif 13 <= age <= 19:
            return AgeGroup.TEEN
        elif 20 <= age <= 29:
            return AgeGroup.YOUNG_ADULT
        elif 30 <= age <= 44:
            return AgeGroup.ADULT
        elif 45 <= age <= 59:
            return AgeGroup.MIDDLE_AGED
        else:
            return AgeGroup.SENIOR