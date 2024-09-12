from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .friend import FriendModelViewSet, FriendRequestModelViewSet
from .profile import ProfileModelViewSet



router = DefaultRouter()
router.register(r"friends", FriendModelViewSet)
router.register(r"profiles", ProfileModelViewSet)
router.register(r"friendrequests", FriendRequestModelViewSet)



urlpatterns = [path("", include(router.urls))]