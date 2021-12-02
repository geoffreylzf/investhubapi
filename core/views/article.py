from core.models.article import Article
from core.serializers.article import ListArticleSerializer, ArticleSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class ArticleViewSet(CReadOnlyModelViewSet):
    queryset = Article.objects.filter(is_publish=True).all()
    serializer_class = ArticleSerializer

    filter_field_contain_list = [
        ("article_title",),
        ("author_first_name", "author__user__first_name")
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return ListArticleSerializer
        return super().get_serializer_class()
