from rest_framework.decorators import api_view
from rest_framework.response import Response

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
