from django.db import models

from core.models import User
from core.models.acc_bank import AccBank
from investhubapi.utils.model import CRUSDModel


class Author(CRUSDModel):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    bio = models.CharField(max_length=500)
    commission_pct = models.IntegerField(default=30)

    acc_bank = models.ForeignKey(AccBank, on_delete=models.DO_NOTHING, db_constraint=False, related_name="%(class)s_related",
                                 blank=True, null=True)
    bank_account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_no = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'author'
        ordering = ['id']
