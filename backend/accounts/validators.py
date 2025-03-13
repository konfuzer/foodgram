import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if username.lower() == "me":
        raise ValidationError("Запрещено использовать me как логин")
    if not re.match(r"^[\w.@+-]+\Z", username):
        raise ValidationError(
            "Требуется соблюдать схему "
            "только из букв, цифр, подчеркиваний,"
            " точек, @, плюсов и дефисов,"
            " без лишних символов"
        )
