from rest_framework.response import Response

from core.models.article import Article
from core.serializers.article import ListArticleSerializer, ArticleSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class ArticleViewSet(CReadOnlyModelViewSet):
    queryset = Article.objects.filter(is_publish=True).order_by('-created_at').all()
    serializer_class = ArticleSerializer

    filter_field_contain_list = [
        ("article_title",),
        ("author_first_name", "author__user__first_name")
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return ListArticleSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        json = serializer.data

        is_show_hidden_content = False

        user = request.user
        if not user.is_anonymous:
            if user.is_author and user.author == instance.author:
                is_show_hidden_content = True

            # TODO check user is donator or not

        if not is_show_hidden_content:
            for p in json['paragraphs']:
                if p['is_supporter_view_only']:
                    p['content'] = None
                    p['article_img_path'] = None

        return Response(json)
