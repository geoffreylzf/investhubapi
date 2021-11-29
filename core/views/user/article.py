from core.models.article import Article
from core.serializers.user.article import UserArticleSerializer
from investhubapi.utils.viewset import CModelViewSet


class UserArticleViewSet(CModelViewSet):
    serializer_class = UserArticleSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Article.objects.filter(author=user.author) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    filter_field_contain_list = [
        ("article_title",),
        ("is_publish",),
    ]
