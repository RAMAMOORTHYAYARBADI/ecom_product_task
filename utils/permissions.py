from rest_framework import permissions
from apps.users.models import *
from django.contrib.auth.models import Group
from rest_framework import exceptions

class Is_SuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id != None:
            groups = User.objects.filter(id = request.user.id).last()
            groupname = Group.objects.filter(id = groups.role_id).values_list("name",flat=True)
            return "ADMIN" in groupname
        else:
            msg = ('You do not allow permissions')
            raise exceptions.PermissionDenied(msg)

class Is_User(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id != None:
            groups = User.objects.filter(id = request.user.id).last()
            groupname = Group.objects.filter(id = groups.role_id).values_list("name",flat=True)
            return "USER" in groupname
        else:
            msg = ('You do not allow permissions')
            raise exceptions.PermissionDenied(msg)
    
class Is_Admin_User(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id != None:
            groups = User.objects.filter(id = request.user.id).last()
            groupname = Group.objects.filter(id = groups.role_id).values_list("name",flat=True)
            return "USER" in groupname or "ADMIN" in groupname
        else:
            msg = ('You do not allow permissions')
            raise exceptions.PermissionDenied(msg)