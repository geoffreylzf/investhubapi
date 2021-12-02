from core.models.stock_counter import StockCounter
from core.serializers.stock_counter import StockCounterSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class StockCounterViewSet(CReadOnlyModelViewSet):
    queryset = StockCounter.objects.all()
    serializer_class = StockCounterSerializer

    filter_field_contain_list = [
        ("stock_code",),
        ("stock_symbol",),
        ("stock_name",),
    ]
