from core.models.stock_counter import StockCounter
from investhubapi.utils.serializer import CModelSerializer


class StockCounterSerializer(CModelSerializer):
    class Meta:
        model = StockCounter
        fields = ('id',
                  'stock_code',
                  'stock_symbol',
                  'stock_name',)
