from rest_framework import serializers

from core.models.sponsor import Sponsor
from investhubapi.utils.serializer import CModelSerializer


class UserSponsorSerializer(CModelSerializer):
    article_title = serializers.ReadOnlyField(source="article.article_title", default=None)
    article_is_publish = serializers.ReadOnlyField(source="article.is_publish", default=None)
    author = serializers.ReadOnlyField(source="article.author.id", default=None)
    author_first_name = serializers.ReadOnlyField(source="article.author.user.first_name", default=None)

    class Meta:
        model = Sponsor
        fields = ('sponsor_date',
                  'article',
                  'article_title',
                  'article_is_publish',
                  'author',
                  'author_first_name',
                  'amt',
                  'payment_type',)
