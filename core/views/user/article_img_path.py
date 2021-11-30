from rest_framework import status
from rest_framework.response import Response

from core.models.article_img import ArticleImg
from core.serializers.user.article_img_path import ArticleImgSerializer
from investhubapi.utils.viewset import CModelViewSet


class UserArticleImgViewSet(CModelViewSet):
    queryset = ArticleImg.objects.all()
    serializer_class = ArticleImgSerializer

    def get_queryset(self):
        user = self.request.user
        qs = ArticleImg.objects.filter(created_by=user) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)

    def update(self, request, *args, **kwargs):
        return Response(status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response(status.HTTP_403_FORBIDDEN)
