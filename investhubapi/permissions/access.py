from rest_framework import permissions

RETRIEVE_METHODS = ['GET']
CREATE_METHODS = ['POST']
UPDATE_METHODS = ['PUT', 'PATCH']
DELETE_METHODS = ['DELETE']

PUBLIC_START_ROUTES = [
    'api/acc/banks/',
    'api/topics/',
    'api/stock/counters/',
    'api/articles/',
    'api/authors/',
]

OPTIONAL_AUTH_ROUTES = [
    'api/articles/<pk>/view/$',
]

REQUIRE_AUTH_ROUTES = [
    'api/articles/<article_id>/comments/$',
    'api/articles/<article_id>/comments/<pk>/$',
    'api/articles/<article_id>/comments/<comment_id>/replies/$',
    'api/articles/<article_id>/comments/<comment_id>/replies/<pk>/$',
]


class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        route = reconstruct_route(request.resolver_match.route)
        method = request.method
        params = request.query_params

        print(route)

        if route.startswith("api/auth/"):
            return True

        if is_start_with_public_routes(route) and method in RETRIEVE_METHODS:
            return True

        if route in OPTIONAL_AUTH_ROUTES:
            return True

        if route in REQUIRE_AUTH_ROUTES and not user.is_anonymous:
            return True

        if route.startswith("api/user/") and not user.is_anonymous:
            return True

        return False


def is_start_with_public_routes(route):
    for r in PUBLIC_START_ROUTES:
        if route.startswith(r):
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
