from core.models.article_img import ArticleImg
from investhubapi.utils.serializer import CModelSerializer


class ArticleImgSerializer(CModelSerializer):
    class Meta:
        model = ArticleImg
        fields = ('id',
                  'path',)
