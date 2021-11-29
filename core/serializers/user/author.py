from rest_framework import serializers

from core.models import Author
from investhubapi.utils.serializer import CModelSerializer


class UserAuthorSerializer(CModelSerializer):
    commission_pct = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = ('bio',
                  'acc_bank', 'bank_account_name', 'bank_account_no',
                  'mobile_no',
                  'commission_pct',)
