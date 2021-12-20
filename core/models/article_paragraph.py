from django.db import models

from core.models.article import Article
from investhubapi.utils.model import CRUSDModel


class ArticleParagraph(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, db_constraint=False, related_name="paragraphs", )
    order = models.IntegerField(default=0)
    content = models.TextField(blank=True, null=True)
    is_supporter_view_only = models.BooleanField(default=False)

    class Meta:
        db_table = 'article_paragraph'
        ordering = ['id']
