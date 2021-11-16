from django.db import models

from core.models import User
from core.models.article import Article
from investhubapi.utils.model import CRUSDModel


class Donate(CRUSDModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="donates", )
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name="donates", )
    amt = models.DecimalField(max_digits=15, decimal_places=2)

    reference_no = models.CharField(max_length=100)

    class Meta:
        db_table = 'donate'
        ordering = ['id']
