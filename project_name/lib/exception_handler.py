from project_name.api import api as app_api
from django.core.exceptions import BadRequest
from django.utils.encoding import force_text


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



"""
    @note: Override default error handler
    # @todo: @see: https://github.com/vitalik/django-ninja/issues/482
"""
@app_api.exception_handler(APPException)
def app_exception_handler(request, exc):
    return app_api.create_response(
        request,
        {"message": exc.message},
        status=exc.status,
    )