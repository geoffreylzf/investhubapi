from django.db import models

from core.models import User
from core.models.article import Article
from investhubapi.utils.model import CRUSDModel


class ArticleView(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name="views", )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="%(class)s_related",
                             blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    view_datetime = models.DateTimeField()

    reference_no = models.CharField(max_length=100)

    class Meta:
        db_table = 'article_view'
        ordering = ['id']
