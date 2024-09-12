from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_synonyms = ["author", "user", "owner", "creator"]

        for synonym in user_synonyms:
            if hasattr(obj, synonym):
                author = getattr(obj, synonym)
                break
        else:

            return False
        return author == request.user or request.user.is_staff