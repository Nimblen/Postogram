from django.core.exceptions import ValidationError

from src.apps.core.validators import FileValidatorBase







class FilePostTypeValidator(FileValidatorBase):
    def __init__(self, post_type: str) -> None:
        self.post_type = post_type
        self.post_type_keys = {
            'image': ['image/jpeg', 'image/png'],
            'video': ['video/mp4'],
            'story': ['image/jpeg', 'image/png', 'video/mp4'],
        }

    def validate(self, file) -> None:
        if file.content_type not in self.post_type_keys[self.post_type]:
            raise ValidationError(
                f"Not allowed content type: {file.content_type} for {self.post_type}"
            )


class PostVideoTypeValidator(FileValidatorBase):
    def __init__(self, post) -> None:
        self.post = post

    def validate(self, file) -> None:
        # Проверка, что у поста уже есть файл и этот файл — видео, или тип поста — "видео"
        # Check that the post already has a file and this file is a video, or the post type is "video"
        if self.post.files.exists() and file.content_type == "video/mp4":
            raise ValidationError(
                f"You can't upload another video for post {self.post.id}"
            )
        if self.post.post_type == "video" and file.content_type != "video/mp4":
            raise ValidationError(
                f"For post {self.post.id}, the post type must be 'video' and the file type must be 'video/mp4'" 

            )