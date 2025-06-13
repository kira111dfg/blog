import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Пароль должен содержать минимум 8 символов."),
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву."),
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну строчную букву."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Пароль должен быть не короче 8 символов, содержать хотя бы одну заглавную и одну строчную букву."
        )
