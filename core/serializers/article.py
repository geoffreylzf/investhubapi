from rest_framework import serializers

from core.models import Author
from core.models.article import Article
from core.models.article_paragraph import ArticleParagraph
from core.models.article_stock import ArticleStockCounter
from core.models.article_topic import ArticleTopic
from core.models.author_follower import AuthorFollower
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
    article_img_path = serializers.ImageField(source="article_img.path", default=None, read_only=True)

    class Meta:
        model = ArticleParagraph
        fields = ('order',
                  'type',
                  'content',
                  'article_img_path',
                  'is_supporter_view_only',)


class ArticleAuthorSerializer(CModelSerializer):
    user = serializers.ReadOnlyField(source="user.id", default=None)
    first_name = serializers.ReadOnlyField(source="user.first_name", default=None)
    img_path = serializers.ImageField(source="user.user_img.path", default=None, read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id',
                  'bio',
                  'user',
                  'first_name',
                  'img_path',
                  'is_following',)

    def get_is_following(self, obj):
        """
        Check is current user if following this author
        return false if no auth
        """
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user and not user.is_anonymous:
            cnt = AuthorFollower.objects.filter(author=obj, user=user).count()
            if cnt > 0:
                return True

        return False


class ArticleSerializer(CModelSerializer):
    author = ArticleAuthorSerializer()
    topics = ArticleTopicSerializer(many=True)
    stock_counters = ArticleStockCounterSerializer(many=True)
    paragraphs = ArticleParagraphSerializer(many=True, )

    class Meta:
        model = Article
        fields = ('id',
                  'author',
                  'article_title',
                  'paragraphs',
                  'topics',
                  'stock_counters',
                  'created_at',
                  'updated_at',)


class ListArticleSerializer(CModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.user.first_name", default=None)
    author_img_path = serializers.ImageField(source="author.user.user_img.path", default=None, read_only=True)

    topics = ArticleTopicSerializer(many=True)
    stock_counters = ArticleStockCounterSerializer(many=True)

    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id',
                  'article_title',
                  'author_first_name',
                  'author_img_path',
                  'topics',
                  'stock_counters',
                  'comment_count',
                  'view_count',
                  'created_at',
                  'updated_at',)

    def get_comment_count(self, obj):
        return obj.comments.count()
