from copy import deepcopy
from src.errors import ERRORS
from src.apps.core.constants import ErrorStatus, LangCode, ErrorType


def get_error_message(code, lang_code, ctx: dict = None) -> tuple:
    messages = ERRORS.get(code)
    message = messages.get(lang_code)
    if ctx:
        message = message.format(**ctx)
    return message, messages.get("status_code")


def format_error_response(
    error_data={},
    exception_instance=None,
    lang_code: str = LangCode.EN,
    error_status: str = ErrorStatus.ERROR,
    error_type: str = ErrorType.SERVER_ERROR,
):
    error_response = list()
    status_code = 500
    error_template = {
        "key": None,
        "code": None,
        "error_status": error_status,
        "error_type": error_type,
        "status_code": status_code,
        "messages": [],
    }

    if error_type == ErrorType.VALIDATION_ERROR:
        status_code = 400
        for key, messages in error_data.items():
            error_template = deepcopy(error_template)
            details = {
                "key": key,
                "messages": messages,
            }
            error_template.update(details)
            error_response.append(error_template)

    else:

        if exception_instance:
            error_code = exception_instance.code
            error_ctx = exception_instance.ctx
            error_lang_code = (
                exception_instance.lang_code
                if exception_instance.lang_code
                else lang_code
            )
            error_status = exception_instance.error_status
            error_message, error_status_code = get_error_message(
                error_code, error_lang_code, ctx=error_ctx
            )
            status_code = error_status_code
            error_template["code"] = error_code
            error_template["messages"] = [error_message]
            error_template["error_status"] = error_status
            error_template["error_type"] = error_type
            error_template["status_code"] = status_code

        error_response.append(error_template)

    return error_template, status_code
