from django.db import models

from investhubapi.utils.model import CRUSDModel


class Topic(CRUSDModel):
    topic_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'topic'
        ordering = ['id']
