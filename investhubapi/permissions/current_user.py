import ipware
from rest_framework import permissions
from threading import local

_user = local()
_ip = local()


def get_current_user():
    return _user.value


def get_current_ip():
    return _ip.value


class CurrentUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        _user.value = request.user

        ip, routable = ipware.get_client_ip(request)
        _ip.value = ip
        return True
