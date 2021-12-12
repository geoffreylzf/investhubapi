from rest_framework import serializers

from core.models import Author
from core.models.author_follower import AuthorFollower
from investhubapi.utils.serializer import CModelSerializer


class AuthorSerializer(CModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name", default=None)
    last_name = serializers.ReadOnlyField(source="user.last_name", default=None)
    img_path = serializers.ImageField(source="user.user_img.path", default=None, read_only=True)

    article_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

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
