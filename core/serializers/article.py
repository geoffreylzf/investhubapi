from rest_framework import serializers

from core.models.article import Article
from core.models.article_stock import ArticleStockCounter
from core.models.article_topic import ArticleTopic
from investhubapi.utils.serializer import CModelSerializer


class ArticleTopicSerializer(CModelSerializer):
    topic_name = serializers.ReadOnlyField(source="topic.topic_name")

    class Meta:
        model = ArticleTopic
        fields = ('topic_name',)


class ArticleStockCounterSerializer(CModelSerializer):
    stock_symbol = serializers.ReadOnlyField(source="stock_counter.stock_symbol")

    class Meta:
        model = ArticleStockCounter
        fields = ('stock_symbol',)


class ArticleSerializer(CModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.user.first_name", default=None)
    author_img_path = serializers.ImageField(source="author.user.user_img.path", default=None, read_only=True)

    topics = ArticleTopicSerializer(many=True)
    stock_counters = ArticleStockCounterSerializer(many=True)

    # TODO view_count, comment_count

    class Meta:
        model = Article
        fields = ('id',
                  'article_title',
                  'author_first_name',
                  'author_img_path',
                  'topics',
                  'stock_counters',
                  'created_at',
                  'updated_at',)


class ListArticleSerializer(CModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.user.first_name", default=None)
    author_img_path = serializers.ImageField(source="author.user.user_img.path", default=None, read_only=True)

    topics = ArticleTopicSerializer(many=True)
    stock_counters = ArticleStockCounterSerializer(many=True)

    # TODO view_count, comment_count

    class Meta:
        model = Article
        fields = ('id',
                  'article_title',
                  'author_first_name',
                  'author_img_path',
                  'topics',
                  'stock_counters',
                  'created_at',
                  'updated_at',)
