from django.db import models

from core.models.article import Article
from investhubapi.utils.model import CRUSDModel


class ArticleParagraph(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name="paragraphs", )
    order = models.IntegerField(default=0)
    content = models.TextField()

    class Meta:
        db_table = 'article_parapgraph'
        ordering = ['id']
