from basic.models import Classroom
from rest_framework import permissions

class IsownerorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user 

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.members.all().filter(username=request.user.username).exists()


        
