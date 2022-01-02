import json

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
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
def login(request):
    provider = request.data.get('provider')
    code = request.data.get('code')

    if provider and code:
        if provider == 'facebook':
            return login_facebook(code)
        elif provider == 'google':
            return login_google(code)

    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response("Please provide email and password", status.HTTP_406_NOT_ACCEPTABLE)

    try:
        user = User.objects.get(email=email, is_active=True,
                                provider_type__isnull=True, provider_id__isnull=True)
        if not user.check_password(password):
            raise User.DoesNotExist
    except User.DoesNotExist:
        raise AuthenticationFailed('No active account found with the given credentials')

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['POST'])
def login_provider(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


def login_facebook(authorization_code):
    provider = settings.OAUTH_PROVIDER

    res_auth = requests.get(provider['FACEBOOK_OAUTH_URL'], {
        'client_id': provider['FACEBOOK_CLIENT_ID'],
        'client_secret': provider['FACEBOOK_CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': provider['FACEBOOK_REDIRECT_URI']
    })
    data_auth = json.loads(res_auth.text)

    res_access = requests.get(provider['FACEBOOK_DATA_URL'], {
        'access_token': data_auth.get('access_token'),
        'fields': provider['FACEBOOK_DATA_FIELDS']
    })

    data = json.loads(res_access.text)

    facebook_id = data.get('id')
    email = data.get('email')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    display_name = data.get('name', '')

    if facebook_id is None:
        return Response("Can not get facebook id", status.HTTP_406_NOT_ACCEPTABLE)
    if email is None:
        return Response("Can not get facebook registered email", status.HTTP_406_NOT_ACCEPTABLE)

    try:
        user = User.objects.get(provider_type='facebook',
                                provider_id=facebook_id)
    except User.DoesNotExist:
        user = None

    if user is None:
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            provider_type='facebook',
            provider_id=facebook_id,
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


def login_google(authorization_code):
    provider = settings.OAUTH_PROVIDER

    res_auth = requests.post(provider['GOOGLE_OAUTH_URL'], {
        'client_id': provider['GOOGLE_CLIENT_ID'],
        'client_secret': provider['GOOGLE_CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': provider['GOOGLE_REDIRECT_URI']
    })
    data_auth = json.loads(res_auth.text)

    res_access = requests.get(provider['GOOGLE_DATA_URL'], {
        'access_token': data_auth.get('access_token'),
    })

    data = json.loads(res_access.text)

    google_id = data.get('id')
    email = data.get('email')
    first_name = data.get('given_name', '')
    last_name = data.get('family_name', '')
    display_name = data.get('name', '')

    if google_id is None:
        return Response("Can not get google id", status.HTTP_406_NOT_ACCEPTABLE)
    if email is None:
        return Response("Can not get google registered email", status.HTTP_406_NOT_ACCEPTABLE)

    try:
        user = User.objects.get(provider_type='google',
                                provider_id=google_id)
    except User.DoesNotExist:
        user = None

    if user is None:
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            provider_type='google',
            provider_id=google_id,
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
