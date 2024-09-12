from rest_framework import viewsets

from src.apps.post.serializers import (
    PostSerializer,
    PostCommentSerializer,
    PostCommentLikeSerializer,
    PostLikeSerializer,
    PostFileSerializer,
)

from src.apps.post.models import Post, PostComment, PostCommentLike, PostLike, PostFile



class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostFileModelViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer


    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        pass


class PostCommentModelViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentLikeModelViewSet(viewsets.ModelViewSet):
    queryset = PostCommentLike.objects.all()
    serializer_class = PostCommentLikeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeModelViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)