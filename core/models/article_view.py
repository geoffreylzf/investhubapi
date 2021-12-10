from datetime import datetime

from django.db import models

from core.models import User
from core.models.article import Article
from investhubapi.utils.manager import ValidManager
from investhubapi.utils.model import CRUSDModel


class CustomManager(ValidManager):
    def create_view_count(self, article, ip_address, user):
        v = self.model(article=article,
                       ip_address=ip_address,
                       created_at=datetime.now())
        v.pure_save = True

        if not user.is_anonymous:
            v.created_by = user

        v.save()


class ArticleView(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, db_constraint=False, related_name="views", )
    ip_address = models.GenericIPAddressField()

    class Meta:
        db_table = 'article_view'
        ordering = ['id']

    objects = CustomManager()
