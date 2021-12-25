from rest_framework import serializers

from core.models import Author
from core.models.article import Article
from core.models.article_paragraph import ArticleParagraph
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


class ArticleParagraphSerializer(CModelSerializer):

    class Meta:
        model = ArticleParagraph
        fields = ('order',
                  'content',
                  'is_supporter_view_only',)


class ArticleAuthorSerializer(CModelSerializer):
    user = serializers.ReadOnlyField(source="user.id", default=None)
    display_name = serializers.ReadOnlyField(source="user.display_name", default=None)
    img_path = serializers.ImageField(source="user.user_img.path", default=None, read_only=True)
    is_following = serializers.SerializerMethodField()
    current_user_support = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id',
                  'bio',
                  'user',
                  'display_name',
                  'img_path',
                  'is_following',
                  'current_user_support',)

    def get_is_following(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return obj.check_is_follower(user)

    def get_current_user_support(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return obj.get_current_user_support_data(user)


class ArticleSerializer(CModelSerializer):
    author = ArticleAuthorSerializer()
    topics = ArticleTopicSerializer(many=True)
    stock_counters = ArticleStockCounterSerializer(many=True)
    paragraphs = ArticleParagraphSerializer(many=True)
    current_user_sponsor = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id',
                  'author',
                  'article_title',
                  'paragraphs',
                  'topics',
                  'stock_counters',
                  'view_count',
                  'current_user_sponsor',
                  'publish_datetime',
                  'created_at',
                  'updated_at',)

    def get_current_user_sponsor(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return obj.get_current_user_sponsor_data(user)


class ListArticleSerializer(CModelSerializer):
    author_display_name = serializers.ReadOnlyField(source="author.user.display_name", default=None)
    author_img_path = serializers.ImageField(source="author.user.user_img.path", default=None, read_only=True)

    topics = ArticleTopicSerializer(many=True)
    stock_counters = ArticleStockCounterSerializer(many=True)

    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id',
                  'article_title',
                  'author_display_name',
                  'author_img_path',
                  'topics',
                  'stock_counters',
                  'comment_count',
                  'view_count',
                  'publish_datetime',
                  'created_at',
                  'updated_at',)

    def get_comment_count(self, obj):
        return obj.comments.count()
