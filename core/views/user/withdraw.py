from datetime import date

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models.author_withdraw import AuthorWithdraw
from core.models.flow_status import Status
from core.serializers.user.withdraw import UserWithdrawSerializer
from investhubapi.utils.viewset import CModelViewSet


class UserWithdrawViewSet(CModelViewSet):
    queryset = AuthorWithdraw.objects.all()
    serializer_class = UserWithdrawSerializer

    filter_field_contain_list = [
        ("withdraw_date",),
        ("author_remark",),
        ("flow_status_desc", "flow_status__desc"),
        ("system_remark",),
        ("reference_no",),
    ]

    def get_queryset(self):
        user = self.request.user
        qs = AuthorWithdraw.objects.filter(author=user.author) \
            .distinct() \
            .order_by('-created_at')
        return super().mixin_get_queryset(qs)

    def create(self, request, *args, **kwargs):
        author = self.request.user.author

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        v_data = serializer.validated_data

        fund_data = author.get_fund_data()
        if fund_data['available_fund'] < 100:
            return Response("Available fund is not allowed to make withdraw",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if 100 > v_data['amt']:
            return Response("Withdraw lowest limit is RM100",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if fund_data['available_fund'] < v_data['amt']:
            return Response("Withdraw amount is more than available fund",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if v_data['flow_status'].id not in [Status.DRAFT, Status.CONFIRM]:
            return Response("Invalid status", status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=author,
                        withdraw_date=date.today())

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=self.get_success_headers(serializer.data))

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        ins = self.get_object()
        if ins.flow_status.id not in [Status.DRAFT]:
            return Response('Only draft status can be delete', status=status.HTTP_403_FORBIDDEN)
        ins.flow_status_id = Status.DELETE
        ins.save()
        return super().destroy(request, *args, **kwargs)

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path="confirm")
    def confirm(self, request, pk):
        instance = self.get_object()
        if instance.flow_status_id == Status.DRAFT:
            instance.flow_status_id = Status.CONFIRM
            instance.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=True, methods=['post'], url_path="unconfirm")
    def unconfirm(self, request, pk):
        instance = self.get_object()
        if instance.flow_status_id == Status.CONFIRM:
            instance.flow_status_id = Status.DRAFT
            instance.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
