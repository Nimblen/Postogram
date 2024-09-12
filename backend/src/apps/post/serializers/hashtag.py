from rest_framework import serializers

from src.apps.post.models import Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Hashtag
        fields = ["id", "name", "created_at", "updated_at", "author"]