from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat




class FileValidatorBase(ABC):
    @abstractmethod
    def validate(self, file) -> None:
        pass


class FileAllowedTypesValidator(FileValidatorBase):
    def __init__(self, allowed_types: list[str] = None) -> None:
        self.allowed_types = allowed_types or ['image/jpeg', 'image/png', 'video/mp4']

    def validate(self, file) -> None:
        if file.content_type not in self.allowed_types:
            raise ValidationError(
                f"Недопустимый тип файла: {file.content_type},  {self.allowed_types} ✔"
            )


class FileSizeValidator(FileValidatorBase):
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size * 1024 * 1024

    def validate(self, file) -> None:
        if file.size > self.max_size:
            raise ValidationError(
                    f'Файл слишком большой. Максимальный размер: {self.max_size / (1024 * 1024) } MB, Ваш файл: {filesizeformat(file.size)}.\
            ')







class FileValidator:
    def __init__(self, validators: list[FileValidatorBase]) -> None:
        self.validators = validators

    def __call__(self, file) -> None:
        for validator in self.validators:
            validator.validate(file)