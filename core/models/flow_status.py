from django.db import models


class FlowStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)

    class Meta:
        db_table = 'flow_status'
        ordering = ['id']


class Status:
    REJECT = 20
    DELETE = 40
    CANCEL = 80
    DRAFT = 100
    CONFIRM = 200
    PROCEED = 500
    COMPLETE = 1000
