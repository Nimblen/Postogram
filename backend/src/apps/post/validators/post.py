from drf_lib.errors.exceptions import CustomException

from src.apps.core.validators import FileValidatorBase
from src.apps.core.constants import PostType


class FilePostTypeValidator(FileValidatorBase):
    def __init__(self, post_type: str) -> None:
        self.post_type = post_type
        self.post_type_keys = {
            PostType.IMAGE: ["image/jpeg", "image/png"],
            PostType.VIDEO: ["video/mp4"],
            PostType.STORY: ["image/jpeg", "image/png", "video/mp4"],
        }

    def validate(self, file) -> None:
        if file.content_type not in self.post_type_keys[self.post_type]:
            raise CustomException(4001)


class PostVideoTypeValidator(FileValidatorBase):
    def __init__(self, post) -> None:
        self.post = post

    def validate(self, file) -> None:
        # Проверка, что у поста уже есть файл и этот файл — видео, или тип поста — "видео"
        # Check that the post already has a file and this file is a video, or the post type is "video"
        if self.post.files.exists() and file.content_type == "video/mp4":
            raise CustomException(
                5003, ctx={"file_type": file.content_type, "post_type": self.post.name}
            )
        if self.post.post_type == PostType.VIDEO and file.content_type != "video/mp4":
            raise CustomException(
                5003, ctx={"file_type": file.content_type, "post_type": self.post.type}
            )
