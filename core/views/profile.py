from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers.user import UserSerializer


@api_view(['GET'])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response({"profile": serializer.data})


# TODO author register
@api_view(['GET', 'POST'])
def author(request):
    if request.method == 'GET':
        print('GET')
    serializer = UserSerializer(request.user)
    return Response({"profile": serializer.data})
