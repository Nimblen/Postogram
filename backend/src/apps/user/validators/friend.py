

from rest_framework.exceptions import ValidationError


from src.apps.user.models import FriendRequest 



class FriendRequestValidator(object):
    def validate(self, request):
        if request.user == request.data.get("to_user"):
            raise ValidationError("You can not send a friend request to yourself")