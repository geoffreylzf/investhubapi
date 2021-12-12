from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.models import Author
from core.models.article import Article
from core.models.author_follower import AuthorFollower
from core.serializers.article import ListArticleSerializer
from core.serializers.author import AuthorSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class AuthorViewSet(CReadOnlyModelViewSet):
    queryset = Author.objects.order_by('-created_at').all()
    serializer_class = AuthorSerializer

    filter_field_contain_list = [
        ("first_name", "user__first_name")
    ]

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path="follow")
    def follow(self, request, pk):
        author = self.get_object()
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        af_list = AuthorFollower.objects.filter(author=author, user=user)
        cnt = af_list.count()

        if cnt == 0:
            AuthorFollower.objects.create(author=author, user=user)
        elif cnt == 1:
            return Response('Already followed', status=status.HTTP_406_NOT_ACCEPTABLE)
        elif cnt > 1:
            for af in af_list:
                af.delete()
            AuthorFollower.objects.create(author=author, user=user)

        return Response()

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path="unfollow")
    def unfollow(self, request, pk):
        author = self.get_object()
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        af_list = AuthorFollower.objects.filter(author=author, user=user)

        for af in af_list:
            af.delete()

        return Response()


class AuthorArticleViewSet(CReadOnlyModelViewSet):
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
