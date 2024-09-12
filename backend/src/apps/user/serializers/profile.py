from rest_framework import serializers

from src.apps.core.validators import FileAllowedTypesValidator, FileSizeValidator, FileValidator
from src.apps.user.models import Profile
from src.apps.user.serializers.friend import FriendSerializer, FriendRequestSerializer
from src.apps.user.serializers.user import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friends = FriendSerializer(many=True, read_only=True)
    friend_requests = FriendRequestSerializer(many=True, read_only=True)
    ip_address = serializers.CharField(read_only=True)
    avatar = serializers.FileField(validators=[
        FileValidator([FileAllowedTypesValidator(allowed_types=['image/jpeg', 'image/png']), FileSizeValidator(max_size=5)])
    ])
    

    class Meta:
        model = Profile
        fields = ["user", "bio", "avatar", "ip_address", "friends", "friend_requests"]
