from django.db import models

from core.models.author import Author
from investhubapi.utils.model import CRUSDModel


class Article(CRUSDModel):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, related_name="articles", )
    article_title = models.CharField(max_length=300)

    is_publish = models.BooleanField(default=False)

    class Meta:
        db_table = 'article'
        ordering = ['id']
