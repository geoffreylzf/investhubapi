from datetime import datetime, timedelta

from django.db.models import Count, Min
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Author
from core.models.article import Article
from core.models.article_view import ArticleView
from core.serializers.author import AuthorSerializer
from core.views.article import ArticleViewSet


@api_view(['GET'])
def newest_articles(request):
    qs = Article.objects \
             .filter(is_publish=True, paragraphs__isnull=False) \
             .distinct() \
             .order_by('-publish_datetime')[:10]

    art_list = []
    for a in qs:
        art_list.append({
            "id": a.id,
            "title": a.article_title,
            "author_first_name": a.author.user.first_name,
            "publish_datetime": a.publish_datetime
        })

    return Response(art_list)


@api_view(['GET'])
def newest_authors(request):
    qs = Article.objects \
             .distinct() \
             .values('author') \
             .filter(is_publish=True) \
             .annotate(min_publish_datetime=Min('publish_datetime')) \
             .order_by('-min_publish_datetime')[:5]

    aut_list = []
    for o in qs:
        aut = Author.objects.get(id=o['author'])

        aut_list.append({
            "id": aut.id,
            "first_name": aut.user.first_name,
            "img_path": request.build_absolute_uri(aut.user.user_img.path.url),
            "first_article_publish_datetime": o['min_publish_datetime'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return Response(aut_list)


@api_view(['GET'])
def trend_articles(request):
    last_15_days = datetime.today() - timedelta(days=7)

    qs = ArticleView.objects \
             .values('article') \
             .filter(article__is_publish=True,
                     created_at__gte=last_15_days) \
             .annotate(count=Count('id')) \
             .order_by('-count')[:5]

    art_list = []
    for o in qs:
        a = Article.objects.get(id=o['article'])
        art_list.append({
            "id": a.id,
            "title": a.article_title,
            "view_count": o['count'],
            "author_first_name": a.author.user.first_name,
            "publish_datetime": a.publish_datetime
        })

    return Response(art_list)


class TimelineArticleViewSet(ArticleViewSet):
    queryset = Article.objects.filter(is_publish=True).order_by('-created_at').all()

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return super().get_queryset()

        qs = Article.objects \
            .filter(is_publish=True,
                    author__in=user.followings.all().values('author')) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)
