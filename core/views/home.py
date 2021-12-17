from datetime import datetime, timedelta

from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Author
from core.models.article import Article
from core.models.article_view import ArticleView
from core.serializers.article import ListArticleSerializer
from core.serializers.author import AuthorSerializer


@api_view(['GET'])
def newest_articles(request):
    qs = Article.objects \
             .filter(is_publish=True, paragraphs__isnull=False) \
             .order_by('-created_at')[:10]
    art_list = ListArticleSerializer(qs, many=True).data
    for art in art_list:
        if art['author_img_path']:
            art['author_img_path'] = request.build_absolute_uri(art['author_img_path'])

    return Response(art_list)


@api_view(['GET'])
def newest_authors(request):
    qs = Author.objects \
             .distinct() \
             .filter(articles__is_publish=True,
                     articles__isnull=False, ) \
             .order_by('-created_at')[:5]
    aut_list = AuthorSerializer(qs, many=True).data
    for aut in aut_list:
        if aut['img_path']:
            aut['img_path'] = request.build_absolute_uri(aut['img_path'])
    return Response(aut_list)


@api_view(['GET'])
def trend_articles(request):
    last_15_days = datetime.today() - timedelta(days=15)

    qs = ArticleView.objects \
             .values('article') \
             .filter(article__is_publish=True,
                     created_at__gte=last_15_days) \
             .annotate(count=Count('id')) \
             .order_by('-count')[:10]

    data = []
    for o in qs:
        data.append(Article.objects.get(id=o['article']))

    art_list = ListArticleSerializer(data, many=True).data
    for art in art_list:
        if art['author_img_path']:
            art['author_img_path'] = request.build_absolute_uri(art['author_img_path'])

    return Response(art_list)
