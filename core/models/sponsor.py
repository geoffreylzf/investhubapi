from django.db import models

from core.models import User
from core.models.article import Article
from investhubapi.utils.model import CRUSDModel


class Sponsor(CRUSDModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name="sponsors", )
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, db_constraint=False, related_name="sponsors", )
    commission_pct = models.IntegerField(default=70)
    amt = models.DecimalField(max_digits=15, decimal_places=2)
    payment_type = models.CharField(max_length=20)
    reference_no = models.CharField(max_length=500)

    class Meta:
        db_table = 'sponsor'
        ordering = ['id']
