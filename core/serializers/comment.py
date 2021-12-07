from rest_framework import serializers

from core.models.comment import Comment
from investhubapi.utils.serializer import CModelSerializer


class CommentSerializer(CModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    user_first_name = serializers.ReadOnlyField(source="user.first_name", default=None)
    user_img_path = serializers.ImageField(source="user.user_img.path", default=None, read_only=True)

    class Meta:
        model = Comment
        fields = ('id',
                  'user',
                  'content',
                  'user_first_name',
                  'user_img_path',
                  'created_at',
                  'updated_at',)
