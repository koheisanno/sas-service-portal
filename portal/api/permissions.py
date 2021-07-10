from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from portal.models import *
from rest_framework.exceptions import PermissionDenied

class IsOfficerOrReadOnly(permissions.BasePermission):
    message = 'You must be an officer to edit.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.userProfile in obj.officers.all()

class IsOfficer(permissions.BasePermission):
    message = 'You must be an officer.'

    def has_object_permission(self, request, view, obj):
        return request.user.userProfile in obj.officers.all()

class EventIsOfficer(permissions.BasePermission):
    message = 'You must be an officer.'

    def has_object_permission(self, request, view, obj):
        return request.user.userProfile in obj.club.officers.all()

def checkIsOfficer(request, obj):
    if not request.user.userProfile in obj.officers.all():
        raise PermissionDenied("You must be an officer of the club.")
