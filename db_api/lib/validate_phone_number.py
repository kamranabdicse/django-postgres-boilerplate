import re
from rest_framework.serializers import ValidationError


def validate_phone_number(phone_number):
    if not phone_number:
        return ""
    phone_number_regex = r"^((\+?98)|0)\d{10}$"
    if re.match(phone_number_regex, phone_number):
        return "0" + str(phone_number[-10:])
    else:
        raise ValidationError({"error": "invalid phone number"})