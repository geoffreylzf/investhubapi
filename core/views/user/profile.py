from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers.author import ProfileAuthorSerializer
from core.serializers.user import UserSerializer


@api_view(['GET', 'PUT'])
def profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response({"profile": serializer.data})
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"profile": serializer.data})


@api_view(['POST'])
def author_registration(request):
    user = request.user
    if not user.is_author:
        serializer = ProfileAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response()
    else:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT'])
def author(request):
    user = request.user
    if request.method == 'GET':
        serializer = ProfileAuthorSerializer(user.author)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProfileAuthorSerializer(user.author, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
