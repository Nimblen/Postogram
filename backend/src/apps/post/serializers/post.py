from rest_framework import serializers
from rest_framework.validators import ValidationError
from src.apps.post.models import (
    Post,
    PostComment,
    PostCommentLike,
    PostFile,
    PostLike,
    Hashtag,
)
from src.apps.core.validators import (
    FileValidator,
    FileSizeValidator,
    FileAllowedTypesValidator,
)
from src.apps.post.validators import FilePostTypeValidator, PostVideoTypeValidator


class PostFileSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = PostFile
        fields = ["id", "name", "file", "post", "author"]

    def validate_file(self, value):
        post_id = self.initial_data.get("post")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post not found")

        validators = [
            FileSizeValidator(max_size=10),
            FileAllowedTypesValidator(),
            FilePostTypeValidator(post_type=post.post_type),
            PostVideoTypeValidator(post),
        ]
        for validator in validators:
            validator.validate(value)

        return value


class PostCommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source="author.username")
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = PostComment
        fields = ["id", "comment", "created_at", "updated_at", "author", "post"]


class PostLikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="user.username")
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = PostLike
        fields = ["id", "created_at", "updated_at", "author", "post"]


class PostCommentLikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comment = serializers.PrimaryKeyRelatedField(queryset=PostComment.objects.all())

    class Meta:
        model = PostCommentLike
        fields = ["id", "created_at", "updated_at", "author", "comment"]


class PostSerializer(serializers.ModelSerializer):
    hashtags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Hashtag.objects.all()
    )
    author = serializers.ReadOnlyField(source="author.username")
    file = serializers.FileField(
        write_only=True,
        required=False,
        validators=[
            FileValidator([FileAllowedTypesValidator(), FileSizeValidator(max_size=10)])
        ],
    )
    files = PostFileSerializer(many=True, read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    likes = PostLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "published",
            "post_type",
            "author",
            "hashtags",
            "file",
            "files",
            "comments",
            "likes",
        ]

    def validate_file(self, file):
        post_type = self.initial_data.get("post_type")
        FilePostTypeValidator(post_type).validate(file)
        return file

    def create(self, validated_data):
        try:
            file = validated_data.pop("file")
        except KeyError:
            raise ValidationError("No file provided.")
        hashtags_data = validated_data.pop("hashtags", None)
        author = validated_data.get("author")
        post = Post.objects.create(**validated_data)
        if hashtags_data:
            post.hashtags.set(hashtags_data)
        PostFile.objects.create(file=file, post=post, author=author)
        return post

    def update(self, instance, validated_data):
        file = validated_data.pop("file", None)
        if file:
            PostFile.objects.create(file=file, post=instance, author=instance.author)
        hashtags_data = validated_data.pop("hashtags", None)
        instance = super().update(instance, validated_data)
        if hashtags_data:
            instance.hashtags.set(hashtags_data)
        return instance
