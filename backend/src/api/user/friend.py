from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from src.apps.user.serializers import FriendSerializer, FriendRequestSerializer

from src.apps.user.permissions import IsRequestOwner
from src.apps.user.models import Friend, FriendRequest




class FriendModelViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(user=self.request.user) | Q(friend=self.request.user))
        )


class FriendRequestModelViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsRequestOwner]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if not user.is_staff:
            queryset = queryset.filter(
                Q(from_user=user) | Q(to_user=user) & Q(status="pending")
            )
        return queryset

    def perform_create(self, serializer):
        if self.request.user == serializer.validated_data["to_user"]:
            return Response(
                {"error": "You can not send a friend request to yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Friend.objects.filter(
            Q(user=serializer.validated_data["to_user"], friend=self.request.user)
            | Q(user=self.request.user, friend=serializer.validated_data["to_user"])
        ).exists():
            return Response(
                {"error": "You are already friends with this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(from_user=self.request.user)
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        serializer.save(from_user=self.request.user)
        return super().perform_update(serializer)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk):
        friend_request = self.get_object()
        if friend_request.to_user != request.user:
            return Response(
                {"error": "You are not allowed to accept this request"},
                status=status.HTTP_403_FORBIDDEN,
            )
        friend_request.accept()
        return Response(
            {"status": "request has been accepted"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def decline(self, request, pk):
        friend_request = self.get_object()
        if friend_request.to_user != request.user:
            return Response(
                {"error": "You are not allowed to decline this request"},
                status=status.HTTP_403_FORBIDDEN,
            )
        friend_request.reject()
        return Response(
            {"status": "request has been declined"}, status=status.HTTP_200_OK
        )
