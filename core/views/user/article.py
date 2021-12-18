from datetime import datetime

from django.db.models import F, Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models.article import Article
from core.models.sponsor import Sponsor
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
        data = serializer.validated_data
        if len(data.get('paragraphs', [])) != 0 and data.get('is_publish', False):
            serializer.save(author=self.request.user.author,
                            publish_datetime=datetime.now())
        else:
            serializer.save(author=self.request.user.author)

    def perform_update(self, serializer):
        ins = self.get_object()
        data = serializer.validated_data
        if not ins.is_publish \
                and ins.publish_datetime is None \
                and data.get('is_publish', False):
            # Save publish_datetime if article not publish before and update to publish now
            serializer.save(publish_datetime=datetime.now())
        else:
            super().perform_update(serializer)

    @action(detail=True, methods=['get'], url_path="statistics")
    def statistics(self, request, pk):
        article = self.get_object()

        amt = Sponsor.objects.filter(article=article) \
                  .aggregate(fund=Sum(F('amt') * F('commission_pct') / 100)) \
                  .get('fund') or 0

        return Response({
            "view_count": article.view_count,
            "comment_count": article.comments.count(),
            "sponsor_count": article.sponsors.count(),
            "sponsor_amt": amt,
        })
