from django.db.models import Sum, F
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models.author_withdraw import AuthorWithdraw
from core.models.sponsor import Sponsor
from core.serializers.user.author import UserAuthorSerializer
from core.serializers.user.user import UserProfileSerializer, UserProfileDataSerializer


@api_view(['GET', 'PUT'])
def profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        data = serializer.data
        if data['user_img_path']:
            data['user_img_path'] = request.build_absolute_uri(data['user_img_path'])
        return Response({"profile": data})
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"profile": serializer.data})


@api_view(['GET'])
def data_(request):
    serializer = UserProfileDataSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def author_registration(request):
    user = request.user
    if not user.is_author:
        serializer = UserAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response()
    else:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT'])
def author(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserAuthorSerializer(user.author)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserAuthorSerializer(user.author, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def author_fund(request):
    fund_data = request.user.author.get_fund_data()

    return Response({
        'available_fund': fund_data['fund'] - fund_data['complete_withdraw'] - fund_data['pending_withdraw'],
        'pending_withdraw': fund_data['pending_withdraw'],
    })
