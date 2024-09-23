


class ErrorType:
    VALIDATION_ERROR = "validation_error"
    DB_ERROR = "database_error"
    PERMISSION_ERROR = "permission_error"
    SERVER_ERROR = "server_error"



class ErrorStatus:
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"



class LangCode:
    EN = "en"
    RU = "ru"




class PostType:
    IMAGE = "IMG"
    VIDEO = "MP4"
    STORY = "STR"

    CHOICES = [
        (IMAGE, "image"),
        (VIDEO, "video"),
        (STORY, "story"),
    ]



class RequestStatus:
    PENDING = "PD"
    ACCEPTED = "AP"
    REJECTED = "RJ"
    REQUEST_STATUS_CHOICES = [
        (PENDING, "pending"),
        (ACCEPTED, "accepted"),
        (REJECTED, "rejected"),
    ]