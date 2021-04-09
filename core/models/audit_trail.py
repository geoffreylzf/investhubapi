from django.db import models

from core.models.user import User


class AuditTrail(models.Model):
    model = models.CharField(max_length=255)
    model_id = models.IntegerField()
    action = models.CharField(max_length=10)
    log = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name="%(class)s_related")
    ip_address = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_audit_trail'
        ordering = ['-id']
