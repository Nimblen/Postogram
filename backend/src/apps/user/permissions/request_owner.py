from rest_framework import permissions





class IsRequestOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return bool(obj.to_user == request.user or request.user.is_staff)