from django.db import models

from core.models import User
from core.models.article import Article
from investhubapi.utils.model import CRUSDModel


class Comment(CRUSDModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name="comments", )
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, db_constraint=False, related_name="comments",
                                blank=True, null=True)

    reply_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_constraint=False, related_name="replies",
                                      blank=True, null=True)
    content = models.CharField(max_length=500)

    class Meta:
        db_table = 'comment'
        ordering = ['id']
