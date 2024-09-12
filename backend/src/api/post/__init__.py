from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .post import (
    PostModelViewSet,
    PostCommentModelViewSet,
    PostCommentLikeModelViewSet,
    PostLikeModelViewSet,
    PostFileModelViewSet,
)
from .hashtag import HashtagModelViewSet


router = DefaultRouter()
router.register(r"posts", PostModelViewSet)
router.register(r"comments", PostCommentModelViewSet)
router.register(r"commentlikes", PostCommentLikeModelViewSet)
router.register(r"likes", PostLikeModelViewSet)
router.register(r"hashtags", HashtagModelViewSet)
router.register(r"files", PostFileModelViewSet)


urlpatterns = [path("", include(router.urls))]
