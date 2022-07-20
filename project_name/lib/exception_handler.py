from rest_framework.views import exception_handler
from rest_framework import exceptions, status
from django.utils.translation import gettext as _
from django.http import JsonResponse
import orjson
import traceback


def get_response(message="", details="", status=False, status_code=200, trace=""):
    return {
        "message": _(message),
        "details": details,
        "status": status,
        "status_code": status_code,
        "trace": trace,
    }


def get_error_details(error_data, error_details=""):
    if isinstance(error_data, str):
        return error_details + _(error_data)
    elif isinstance(error_data, dict):
        for k, v in error_data.items():
            error_details = get_error_details(v, error_details + _(k) + ": ")
    elif isinstance(error_data, list):
        for i in error_data:
            error_details = get_error_details(i, error_details)

    return error_details


def handle_exception(exc, context):
    error_response = exception_handler(exc, context)
    if error_response is not None:
        if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
            error_response.status_code = status.HTTP_401_UNAUTHORIZED
        error = error_response.data
        error_response.data = get_response(
            message=exc.__class__.__name__,
            details=get_error_details(error),
            status_code=error_response.status_code,
            trace=orjson.dumps(traceback.format_stack()).decode()
        )
    else:
        error_response_data = get_response(
            message="Internal server error",
            details=exc.__class__.__name__ + ": " + str(exc),
            status_code=500,
            trace=traceback.format_exc()
        )
        error_response = JsonResponse(error_response_data, status=error_response_data["status_code"])

    return error_response


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = get_response(
                message="Page not found, invalid url", status_code=response.status_code
            )
            return JsonResponse(response, status=response["status_code"])

        return response
