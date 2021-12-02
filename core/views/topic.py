from core.models.topic import Topic
from core.serializers.topic import TopicSerializer
from investhubapi.utils.viewset import CReadOnlyModelViewSet


class TopicViewSet(CReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    filter_field_contain_list = [
        ("topic_name",),
    ]
