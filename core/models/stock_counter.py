from django.db import models

from investhubapi.utils.model import CRUSDModel


class StockCounter(CRUSDModel):
    stock_code = models.CharField(max_length=20)
    stock_symbol = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'stock_counter'
        ordering = ['id']
