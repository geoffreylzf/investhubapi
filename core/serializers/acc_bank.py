from core.models.acc_bank import AccBank
from investhubapi.utils.serializer import CModelSerializer


class AccBankSerializer(CModelSerializer):
    class Meta:
        model = AccBank
        fields = ('id',
                  'acc_bank_code', 'acc_bank_name')
