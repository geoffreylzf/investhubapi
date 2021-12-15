from core.models.sponsor import Sponsor
from investhubapi.utils.serializer import CModelSerializer


class SponsorPaymentSerializer(CModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('article',
                  'amt',
                  'payment_type',)
