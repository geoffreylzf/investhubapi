from django.conf import settings
from rest_framework import permissions

ALWAYS_ALLOW_ROUTES = [
    'api/auth/user/',
    'api/auth/change-password/',
]

RETRIEVE_METHODS = ['GET']
CREATE_METHODS = ['POST']
UPDATE_METHODS = ['PUT', 'PATCH']
DELETE_METHODS = ['DELETE']


class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        route = reconstruct_route(request.resolver_match.route)
        method = request.method
        params = request.query_params

        if settings.DEBUG:
            return True

        if user.is_anonymous:
            return False

        if route in ALWAYS_ALLOW_ROUTES:
            return True

        if user.is_superuser:
            return True

        return False


def reconstruct_route(route):
    regex_start = route.find("(")
    regex_end = route.find(")")

    if regex_start == -1:
        return route
    else:
        regex = route[regex_start:regex_end + 1]
        param_start = regex.find("<")
        param_end = regex.find(">")
        param = regex[param_start:param_end + 1]
        return reconstruct_route(route.replace(regex, param))
