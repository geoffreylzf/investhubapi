from django.db import models

from core.models.article import Article
from core.models.topic import Topic
from investhubapi.utils.model import CRUSDModel


class ArticleStockTopic(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name="topics", )
    stock_counter = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name="%(class)s_related", )

    class Meta:
        db_table = 'article_topic'
        ordering = ['id']
