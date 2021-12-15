from datetime import date

from django.db import models
from django.db.models import F, Sum

from core.models import User
from core.models.acc_bank import AccBank
from core.models.flow_status import Status
from investhubapi.utils.model import CRUSDModel


class Author(CRUSDModel):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    bio = models.CharField(max_length=500)
    commission_pct = models.IntegerField(default=70)

    acc_bank = models.ForeignKey(AccBank, on_delete=models.DO_NOTHING, db_constraint=False,
                                 related_name="%(class)s_related",
                                 blank=True, null=True)
    bank_account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_no = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'author'
        ordering = ['id']

    def check_is_follower(self, user):
        if user and not user.is_anonymous:
            from core.models.author_follower import AuthorFollower
            cnt = AuthorFollower.objects.filter(author=self, user=user).count()
            if cnt > 0:
                return True

        return False

    def get_current_user_support_data(self, user):
        is_support = False
        last_date = None
        remaining_days = None

        if user and not user.is_anonymous:
            from core.models.sponsor import Sponsor
            sponsor = Sponsor.objects \
                .filter(user=user, article__in=self.articles.all()) \
                .order_by('-sponsor_date') \
                .first()

            if sponsor:
                diff = date.today() - sponsor.sponsor_date
                if diff.days <= 30:
                    is_support = True
                    last_date = sponsor.sponsor_date
                    remaining_days = 30 - diff.days

        return {
            "is_support": is_support,
            "last_date": last_date,
            "remaining_days": remaining_days
        }

    def get_fund_data(self):
        from core.models.sponsor import Sponsor
        from core.models.author_withdraw import AuthorWithdraw

        fund = Sponsor.objects.filter(article__author=self) \
            .aggregate(fund=Sum(F('amt') * F('commission_pct') / 100)) \
            .get('fund', 0)

        complete_withdraw = 0
        pending_withdraw = 0

        withdraw_qs = AuthorWithdraw.objects \
            .filter(author=self) \
            .values('flow_status_id') \
            .annotate(ttl_amt=Sum('amt'))

        for wd in withdraw_qs:
            fs_id = wd['flow_status_id']
            amt = wd['ttl_amt']
            if fs_id in [Status.DRAFT, Status.CONFIRM, Status.PROCEED]:
                pending_withdraw += amt
            elif fs_id in [Status.COMPLETE]:
                complete_withdraw += amt

        return {
            "fund": fund,
            "complete_withdraw": complete_withdraw,
            "pending_withdraw": pending_withdraw
        }
