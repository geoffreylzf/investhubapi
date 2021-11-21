from django.db import models

from core.models import User
from core.models.author import Author
from investhubapi.utils.model import CRUSDModel


class AuthorFollower(CRUSDModel):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, related_name="followers", )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="followings", )

    class Meta:
        db_table = 'author_follower'
        ordering = ['id']
