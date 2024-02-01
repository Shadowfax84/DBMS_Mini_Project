from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                _("The password must be at least 10 characters long."),
                code='password_too_short',
            )
        if len(password) > 20:
            raise ValidationError(
                _("The password must be at most 20 characters long."),
                code='password_too_long',
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("The password must contain at least one digit."),
                code='password_no_digit',
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
        if not any(char in r"!@#$%^&*()-_=+[]{};:'\"|,.<>/?`~" for char in password):
            raise ValidationError(
                _("The password must contain at least one special character."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one numeric, special character, one capital letter, and should be between 10-20 characters."
        )
