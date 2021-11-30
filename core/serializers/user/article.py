from django.db import transaction
from rest_framework import serializers

from core.models.article import Article
from core.models.article_paragraph import ArticleParagraph
from core.models.article_stock import ArticleStockCounter
from core.models.article_topic import ArticleTopic
from investhubapi.utils.serializer import CModelSerializer


class UserArticleTopicSerializer(CModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    topic_name = serializers.ReadOnlyField(source="topic.topic_name")

    class Meta:
        model = ArticleTopic
        fields = ('id',
                  'topic', 'topic_name')


class UserArticleStockCounterSerializer(CModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    stock_code = serializers.ReadOnlyField(source="stock_counter.stock_code")
    stock_symbol = serializers.ReadOnlyField(source="stock_counter.stock_symbol")
    stock_name = serializers.ReadOnlyField(source="stock_counter.stock_name")

    class Meta:
        model = ArticleStockCounter
        fields = ('id',
                  'stock_counter',
                  'stock_code', 'stock_symbol', 'stock_name')


class UserArticleParagraphSerializer(CModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    article_img_path = serializers.ImageField(source="article_img.path", default=None, read_only=True)

    class Meta:
        model = ArticleParagraph
        fields = ('id',
                  'order',
                  'type',
                  'content',
                  'article_img', 'article_img_path',
                  'is_supporter_view_only',)


class UserArticleSerializer(CModelSerializer):
    paragraphs = UserArticleParagraphSerializer(many=True, required=False)
    topics = UserArticleTopicSerializer(many=True, required=False)
    stock_counters = UserArticleStockCounterSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = ('id',
                  'article_title',
                  'is_publish',
                  'paragraphs',
                  'topics',
                  'stock_counters',
                  'created_at',
                  'updated_at',)

    def to_representation(self, instance):
        art = super().to_representation(instance)
        art['paragraphs'] = sorted(art['paragraphs'], key=lambda x: x['order'])
        return art

    @transaction.atomic
    def create(self, validated_data):
        paragraphs = validated_data.pop('paragraphs', [])
        topics = validated_data.pop('topics', [])
        stock_counters = validated_data.pop('stock_counters', [])

        instance = Article.objects.create(**validated_data)

        instance.create_child_list(child_data=paragraphs,
                                   child_class=ArticleParagraph,
                                   fk_field='article')
        instance.create_child_list(child_data=topics,
                                   child_class=ArticleTopic,
                                   fk_field='article')
        instance.create_child_list(child_data=stock_counters,
                                   child_class=ArticleStockCounter,
                                   fk_field='article')

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        paragraphs = validated_data.pop('paragraphs', [])
        topics = validated_data.pop('topics', [])
        stock_counters = validated_data.pop('stock_counters', [])

        instance.update(**validated_data)
        instance.update_child_list(child_data=paragraphs,
                                   child_class=ArticleParagraph,
                                   fk_field='article')
        instance.update_child_list(child_data=topics,
                                   child_class=ArticleTopic,
                                   fk_field='article')
        instance.update_child_list(child_data=stock_counters,
                                   child_class=ArticleStockCounter,
                                   fk_field='article')

        return instance


class ListUserArticleSerializer(CModelSerializer):
    class Meta:
        model = Article
        fields = ('id',
                  'article_title',
                  'is_publish',
                  'created_at',
                  'updated_at',)
