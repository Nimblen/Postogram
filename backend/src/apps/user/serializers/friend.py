from rest_framework import serializers
from src.apps.user.models import Friend, FriendRequest
from django.contrib.auth.models import User




class FriendSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    friend = serializers.ReadOnlyField(source="friend.username")

    class Meta:
        model = Friend
        fields = ["id", "user", "friend", "created_at"]


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source="from_user.username")
    status = serializers.ReadOnlyField(source="get_status_display")
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "created_at", "status"]

    def create(self, validated_data):
        from_user = validated_data.get("from_user")
        to_user = validated_data.get("to_user")
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("You already sent a friend request to this user.")
        return super().create(validated_data)
    
    


    def validate_to_user(self, value):
            if value == self.context['request'].user:
                raise serializers.ValidationError("Невозможно отправить запрос самому себе.")
            return value