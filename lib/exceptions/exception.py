from django.core.exceptions import BadRequest
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _


class APPException(BadRequest):
    status = 404

    def __init__(self, *args, **kwargs):
        # @note to prevent `Replacement index 0 out of range for positional args tuple` error
        # While we call exception without any parameters
        if args or kwargs:
            self.message = force_text(self.message).format(*args, **kwargs)
        else:
            self.message = force_text(self.message)

    def __str__(self):
        return self.message


class InvalidEmail(Exception):
    pass

