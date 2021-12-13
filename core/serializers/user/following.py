from rest_framework import serializers

from core.models import Author
from investhubapi.utils.serializer import CModelSerializer


class FollowingSerializer(CModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name", default=None)
    last_name = serializers.ReadOnlyField(source="user.last_name", default=None)
    img_path = serializers.ImageField(source="user.user_img.path", default=None, read_only=True)

    article_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_following = serializers.BooleanField(default=True)

    class Meta:
        model = Author
        fields = ('id',
                  'first_name',
                  'last_name',
                  'img_path',
                  'bio',
                  'created_at',
                  'article_count',
                  'follower_count',
                  'is_following',)

    def get_article_count(self, obj):
        return obj.articles.count()

    def get_follower_count(self, obj):
        return obj.followers.count()

