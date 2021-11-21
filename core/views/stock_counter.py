from core.models.stock_counter import StockCounter
from core.serializers.stock_counter import StockCounterSerializer
from investhubapi.utils.viewset import CModelViewSet


class StockCounterViewSet(CModelViewSet):
    queryset = StockCounter.objects.all()
    serializer_class = StockCounterSerializer

    filter_field_contain_list = [
        ("stock_code",),
        ("stock_symbol",),
        ("stock_name",),
    ]
