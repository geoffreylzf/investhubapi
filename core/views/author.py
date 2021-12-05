from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.models import Author
from core.models.article import Article
from core.serializers.article import ListArticleSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class AuthorNewArticleViewSet(CReadOnlyModelViewSet):
    queryset = Article.objects.filter(is_publish=True).order_by('-created_at').all()
    serializer_class = ListArticleSerializer
    author = None

    filter_field_custom_list = [
        ("$_exclude_article", lambda qs, x: qs
         .exclude(id=x)),
    ]

    def get_queryset(self):
        self.author = get_object_or_404(Author, pk=self.kwargs.get('author_id'))
        return super().get_queryset().filter(author=self.author)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
