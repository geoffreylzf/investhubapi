from core.models.user_img import UserImg
from investhubapi.utils.serializer import CModelSerializer


class UserImgPathSerializer(CModelSerializer):
    class Meta:
        model = UserImg
        fields = ('id',
                  'path',)
