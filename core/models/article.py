from datetime import date

from django.db import models

from core.models.author import Author
from investhubapi.utils.model import CRUSDModel


class Article(CRUSDModel):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, db_constraint=False, related_name="articles", )
    article_title = models.CharField(max_length=300)

    is_publish = models.BooleanField(default=False)
    publish_datetime = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'article'
        ordering = ['id']

    def increase_view_count(self):
        self.pure_save = True
        self.view_count += 1
        self.save()

    def get_current_user_sponsor_data(self, user):
        is_sponsor = False
        last_date = None
        remaining_days = None

        if user and not user.is_anonymous:
            from core.models.sponsor import Sponsor
            sponsor = Sponsor.objects \
                .filter(user=user, article=self) \
                .order_by('-sponsor_date') \
                .first()

            if sponsor:
                diff = date.today() - sponsor.sponsor_date
                if diff.days <= 30:
                    is_sponsor = True
                    last_date = sponsor.sponsor_date
                    remaining_days = 30 - diff.days

        return {
            "is_sponsor": is_sponsor,
            "last_date": last_date,
            "remaining_days": remaining_days
        }
