from django.db import models
from django.conf import settings
from src.apps.core.constants import RequestStatus


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_requests"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_requests",
    )
    
    status = models.CharField(
        max_length=10, choices=RequestStatus.REQUEST_STATUS_CHOICES, default=RequestStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

    def accept(self):
        self.status = RequestStatus.ACCEPTED
        self.save()
        Friend.objects.create(user=self.from_user, friend=self.to_user)
        Friend.objects.create(user=self.to_user, friend=self.from_user)
        self.delete()

    def reject(self):
        self.status = RequestStatus.REJECTED
        self.save()


class Friend(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends"
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend_of"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "friend")

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"
