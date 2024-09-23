from django.db import models
from django.conf import settings




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=600, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    ip_address = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username