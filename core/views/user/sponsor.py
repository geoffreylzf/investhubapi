from core.models.sponsor import Sponsor
from core.serializers.user.sponsor import UserSponsorSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class UserSponsorViewSet(CReadOnlyModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = UserSponsorSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Sponsor.objects.filter(user=user) \
            .distinct() \
            .order_by('-sponsor_date')
        return super().mixin_get_queryset(qs)

    filter_field_contain_list = [
        ("article_title", "article__article_title"),
        ("author_first_name", "article__author__first_name")
    ]

    filter_field_equal_list = [
        ("article_is_publish", "article__is_publish"),
    ]
