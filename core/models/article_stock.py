from django.db import models

from core.models.article import Article
from core.models.stock_counter import StockCounter
from investhubapi.utils.model import CRUSDModel


class ArticleStockCounter(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, db_constraint=False, related_name="stock_counters", )
    stock_counter = models.ForeignKey(StockCounter, on_delete=models.DO_NOTHING, db_constraint=False, related_name="%(class)s_related", )

    class Meta:
        db_table = 'article_stock_counter'
        ordering = ['id']
