from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.db.utils import IntegrityError
from django.db.models.deletion import ProtectedError
from django.db.utils import DatabaseError
from django.http import Http404
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
)
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework.response import Response
from rest_framework.views import exception_handler
import logging

from src.apps.core.constants import ErrorType, LangCode

from .exceptions import CustomException
from .error_format import format_error_response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    lang_code = LangCode.RU
    if request := context.get("request", None):
        lang_code = request.headers.get("Accept-Language", LangCode.RU)

    if isinstance(exc, (DjangoPermissionDenied, DRFPermissionDenied)):
        exc = CustomException(2001)
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorType.PERMISSION_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)
    if isinstance(exc, DatabaseError):
        if isinstance(exc, IntegrityError):
            print(exc)
            exc = CustomException(1003)
            error_response, status_code = format_error_response(
                exception_instance=exc,
                error_type=ErrorType.DB_ERROR,
                lang_code=lang_code,
            )
            return Response(error_response, status=status_code)
        exc = CustomException(1004)
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorType.DB_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)

    if isinstance(exc, CustomException):
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorType.SERVER_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        exc = CustomException(2002)
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorType.PERMISSION_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)

    if isinstance(exc, Http404):
        error_response, status_code = format_error_response(
            response.data, lang_code=lang_code
        )
        return Response(error_response, status=404)

    if isinstance(exc, ProtectedError):
        exc = CustomException(2001)
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorType.SERVER_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)

    if isinstance(exc, APIException):
        error_response, status_code = format_error_response(
            response.data, lang_code=lang_code
        )
        return Response(error_response, status=status_code)

    if response is None:
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorType.SERVER_ERROR,
            lang_code=lang_code,
        )
    logger.error(f"Exception: {exc}, Context: {context}")
    return response
