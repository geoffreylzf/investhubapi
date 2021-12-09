from rest_framework import serializers

from core.models import Author
from investhubapi.utils.serializer import CModelSerializer


class AuthorSerializer(CModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name", default=None)
    img_path = serializers.ImageField(source="user.user_img.path", default=None, read_only=True)

    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id',
                  'first_name',
                  'img_path',
                  'bio',
                  'article_count',
                  'created_at',)

    def get_article_count(self, obj):
        return obj.articles.count()
