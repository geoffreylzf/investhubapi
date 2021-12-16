from rest_framework import serializers

from core.models.author_withdraw import AuthorWithdraw
from investhubapi.utils.serializer import CModelSerializer


class UserWithdrawSerializer(CModelSerializer):
    withdraw_date = serializers.ReadOnlyField()
    flow_status_desc = serializers.ReadOnlyField(source="flow_status.desc", default=None)
    system_remark = serializers.ReadOnlyField()
    reference_no = serializers.ReadOnlyField()

    class Meta:
        model = AuthorWithdraw
        fields = ('id',
                  'withdraw_date',
                  'amt',
                  'author_remark',
                  'flow_status',
                  'flow_status_desc',

                  'system_remark',
                  'reference_no',)
