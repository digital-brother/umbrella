from rest_framework import permissions
from django.contrib.auth import get_user_model

from umbrella.contracts.models import Tag

User = get_user_model()


class TagPermissions(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in {"POST", }:
            type = request.data.get('type', None)
            if type and type != Tag.TagTypes.OTHERS:
                return False
        return True


    def has_object_permission(self, request, view, obj):
        user = User.objects.get(id=request.user.id)
        if request.method in {"PATCH",  "PUT", "DELETE"}:
            if obj.type == Tag.TagTypes.OTHERS:
                return True
            contracts = request.data.get('contracts', None)
            if contracts and len(request.data) == 1:
                return True
        return False