from rest_framework import status
from rest_framework.decorators import action
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

    @action(detail=True, methods=['post'], url_path="statistics")
    def statistics(self, request, pk):
        article = self.get_object()

        return Response({
            "view_count": 0,
            "comment_count": 0,
            "sponsor_count": 0,
            "sponsor_amt": 0,
        })
