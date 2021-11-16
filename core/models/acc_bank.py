from django.db import models

from investhubapi.utils.model import CRUSDModel


class AccBank(CRUSDModel):
    acc_bank_code = models.CharField(max_length=20)
    acc_bank_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_bank'
        ordering = ['id']
