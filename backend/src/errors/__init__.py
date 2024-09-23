ERROR_START_NUMBERS = {
    1: "core",
    2: "user",
    3: "friend",
    4: "file",
    5: "post",

}

from .core import ERRORS as CORE_ERRORS
from .file import ERRORS as FILE_ERRORS
from .user import ERRORS as USER_ERRORS
from .friend import ERRORS as FRIEND_ERRORS
from .post import ERRORS as POST_ERRORS

# collect all errors
ERRORS = dict()

ERRORS.update(CORE_ERRORS)
ERRORS.update(FILE_ERRORS)
ERRORS.update(USER_ERRORS)
ERRORS.update(FRIEND_ERRORS)
ERRORS.update(POST_ERRORS)

