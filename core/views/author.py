from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.models import Author
from core.models.article import Article
from core.serializers.article import ListArticleSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class AuthorNewArticleViewSet(CReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ListArticleSerializer

    filter_field_custom_list = [
        ("$_exclude_article_id", lambda qs, x: qs
         .exclude(id=x)),
    ]

    def get_author(self):
        return get_object_or_404(Author, pk=self.kwargs.get('author_id'))

    def get_queryset(self):
        qs = Article.objects \
            .filter(is_publish=True, author=self.get_author()) \
            .order_by('-created_at').all()
        return super().mixin_get_queryset(qs)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

# TODO AuthorHotArticleViewSet
