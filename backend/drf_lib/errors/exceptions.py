from src.apps.core.constants import ErrorStatus, LangCode


class CustomException(Exception):
    def __init__(
        self,
        code: int = 1000,
        message: str = "",
        lang_code: str = LangCode.EN,
        ctx: dict = None,
        error_status: str = ErrorStatus.ERROR,
    ):
        self.code = code
        self.message = message
        self.lang_code = lang_code
        self.ctx = ctx
        self.error_status = error_status
        super().__init__(message)
