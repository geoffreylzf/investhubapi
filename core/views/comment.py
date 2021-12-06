from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.models.article import Article
from core.models.comment import Comment
from core.serializers.comment import CommentSerializer
from investhubapi.utils.viewset import CModelViewSet


class ArticleCommentViewSet(CModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_article(self):
        return get_object_or_404(Article, pk=self.kwargs.get('article_id'))

    def get_queryset(self):
        qs = Comment.objects.filter(article=self.get_article()) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        article=self.get_article())

    def update(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return Response('Owner mismatch', status=status.HTTP_406_NOT_ACCEPTABLE)
        if self.get_object().article != self.get_article():
            return Response('Article mismatch', status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)
