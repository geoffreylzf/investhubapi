from rest_framework import status
from rest_framework.response import Response

from core.models.article import Article
from core.serializers.user.article import UserArticleSerializer, ListUserArticleSerializer
from investhubapi.utils.viewset import CModelViewSet


class UserArticleViewSet(CModelViewSet):
    queryset = Article.objects.all()
    serializer_class = UserArticleSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Article.objects.filter(author=user.author) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)

    filter_field_contain_list = [
        ("article_title",),
    ]

    filter_field_equal_list = [
        ("is_publish",),
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return ListUserArticleSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if self.get_object().author != user.author:
            return Response('You are not the owner of this article', status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if self.get_object().author != user.author:
            return Response('You are not the owner of this article', status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)


