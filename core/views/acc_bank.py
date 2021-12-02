from core.models.acc_bank import AccBank
from core.serializers.acc_bank import AccBankSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class AccBankViewSet(CReadOnlyModelViewSet):
    queryset = AccBank.objects.all().order_by('acc_bank_code')
    serializer_class = AccBankSerializer

    filter_field_contain_list = [
        ("acc_bank_code",),
        ("acc_bank_name",),
    ]
