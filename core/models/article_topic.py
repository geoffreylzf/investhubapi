from django.db import models

from core.models.article import Article
from core.models.topic import Topic
from investhubapi.utils.model import CRUSDModel


class ArticleTopic(CRUSDModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, db_constraint=False, related_name="topics", )
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, db_constraint=False, related_name="%(class)s_related", )

    class Meta:
        db_table = 'article_topic'
        ordering = ['id']
