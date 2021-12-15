from django.db import models

from core.models.author import Author
from core.models.flow_status import FlowStatus, Status
from investhubapi.utils.model import CRUSDModel


class AuthorWithdraw(CRUSDModel):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, db_constraint=False, related_name="withdraws", )
    withdraw_date = models.DateField()
    amt = models.DecimalField(max_digits=15, decimal_places=2)
    author_remark = models.CharField(max_length=500, blank=True, null=True)
    flow_status = models.ForeignKey(FlowStatus, on_delete=models.DO_NOTHING, db_constraint=False,  default=Status.DRAFT, related_name="%(class)s_related")

    system_remark = models.CharField(max_length=500, blank=True, null=True)
    reference_no = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'author_withdraw'
        ordering = ['id']
