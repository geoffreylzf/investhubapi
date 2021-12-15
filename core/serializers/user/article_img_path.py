from core.models.article_img import ArticleImg
from investhubapi.utils.serializer import CModelSerializer


class UserArticleImgSerializer(CModelSerializer):
    class Meta:
        model = ArticleImg
        fields = ('id',
                  'path',)
