import json

import requests
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User


# @api_view(['POST'])
# def change_password(request):
#     data = request.data
#     old_password = data.get('old_password')
#
#     user = get_object_or_404(User, pk=request.user.id)
#
#     if not user.check_password(old_password):
#         return Response("Old password is invalid", status.HTTP_406_NOT_ACCEPTABLE)
#     else:
#         new_password = data.get('new_password')
#         retype_password = data.get('retype_password')
#         if new_password is None or retype_password is None:
#             return Response("New password and retype password is required", status.HTTP_406_NOT_ACCEPTABLE)
#         if new_password != retype_password:
#             return Response("New password and retype password must be same", status.HTTP_406_NOT_ACCEPTABLE)
#         if old_password == new_password:
#             return Response("New password cannot same as old password", status.HTTP_406_NOT_ACCEPTABLE)
#
#         user.set_password(new_password)
#         user.save()
#
#     return Response("Password changed")


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_facebook(request):
    access_token = request.data.get('access_token')
    if access_token is None:
        return Response("Please provide access_token", status.HTTP_406_NOT_ACCEPTABLE)

    res = requests.get('https://graph.facebook.com/v6.0/me', {
        'access_token': access_token,
        'fields': 'id, email, first_name, last_name, name'
    })

    data = json.loads(res.text)

    if res.status_code != 200:
        print(res.text)
        return Response(data, res.status_code)

    email = data.get('email')
    if email is None:
        return Response("Can not get facebook registered email", status.HTTP_406_NOT_ACCEPTABLE)

    try:
        user = User.objects.get(email=email)
        if user.is_staff or user.is_superuser:
            return Response("Forbidden Account", status.HTTP_403_FORBIDDEN)

    except User.DoesNotExist:
        user = None

    if user is None:
        user = User.objects.create_user(
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
