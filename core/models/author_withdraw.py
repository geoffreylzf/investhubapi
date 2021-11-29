from django.db import models

from core.models.author import Author
from investhubapi.utils.model import CRUSDModel


class AuthorWithdraw(CRUSDModel):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, db_constraint=False, related_name="withdraws", )
    amt = models.DecimalField(max_digits=15, decimal_places=2)
    is_complete = models.BooleanField(default=False)
    reference_no = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'author_withdraw'
        ordering = ['id']
