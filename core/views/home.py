from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def newest_articles(request):
    return Response("newest_articles")


@api_view(['GET'])
def newest_authors(request):
    # got at least 1 publish articles
    return Response("newest_authors")


@api_view(['GET'])
def trend_articles(request):
    return Response("month_top_articles")
