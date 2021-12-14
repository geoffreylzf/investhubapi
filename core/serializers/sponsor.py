from core.models.sponsor import Sponsor
from investhubapi.utils.serializer import CModelSerializer


class TestSponsorSerializer(CModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('article',
                  'amt',
                  'payment_type',)
