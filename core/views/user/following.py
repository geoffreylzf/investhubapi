from rest_framework import status
from rest_framework.response import Response

from core.models import Author
from core.serializers.user.following import FollowingSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class FollowingViewSet(CReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = FollowingSerializer

    filter_field_contain_list = [
        ("first_name", "user__first_name")
    ]

    def get_queryset(self):
        user = self.request.user
        qs = Author.objects \
            .filter(followers__deleted_at__isnull=True,
                    followers__user=user) \
            .distinct() \
            .order_by('-followers__created_at')
        return super().mixin_get_queryset(qs)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)
