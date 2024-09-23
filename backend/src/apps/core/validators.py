from abc import ABC, abstractmethod
from django.template.defaultfilters import filesizeformat

from drf_lib.errors.exceptions import CustomException


class FileValidatorBase(ABC):
    @abstractmethod
    def validate(self, file) -> None:
        pass


class FileAllowedTypesValidator(FileValidatorBase):
    def __init__(self, allowed_types: list[str] = None) -> None:
        self.allowed_types = allowed_types or ["image/jpeg", "image/png", "video/mp4"]

    def validate(self, file) -> None:
        if file.content_type not in self.allowed_types:
            raise CustomException(4001)


class FileSizeValidator(FileValidatorBase):
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size * 1024 * 1024

    def validate(self, file) -> None:
        if file.size > self.max_size:
            raise CustomException(
                4000, ctx={"file_max_size": filesizeformat(self.max_size)}
            )


class FileValidator:
    def __init__(self, validators: list[FileValidatorBase]) -> None:
        self.validators = validators

    def __call__(self, file) -> None:
        for validator in self.validators:
            validator.validate(file)
