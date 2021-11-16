from django.db import models

from investhubapi.utils.model import CRUSDModel


class AccWithdraw(CRUSDModel):
    withdraw_date = models.DateField()
    amt = models.DecimalField(max_digits=15, decimal_places=2)
    reference_no = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_withdraw'
        ordering = ['id']
