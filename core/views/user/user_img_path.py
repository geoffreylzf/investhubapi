from rest_framework import status
from rest_framework.response import Response

from core.models.user_img import UserImg
from core.serializers.user.user_img_path import UserImgPathSerializer
from investhubapi.utils.viewset import CModelViewSet


class UserImgPathViewSet(CModelViewSet):
    queryset = UserImg.objects.all()
    serializer_class = UserImgPathSerializer

    def get_queryset(self):
        user = self.request.user
        qs = UserImg.objects.filter(created_by=user) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)

    def update(self, request, *args, **kwargs):
        return Response(status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status.HTTP_403_FORBIDDEN)
