from rest_framework import viewsets
from src.apps.user.serializers import ProfileSerializer


from src.apps.user.models import Profile







class ProfileModelViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, ip_address=self.request.META["REMOTE_ADDR"]
        )
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_update(serializer)
