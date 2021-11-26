from core.models.topic import Topic
from core.serializers.topic import TopicSerializer
from investhubapi.utils.viewset import CModelViewSet


class TopicViewSet(CModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    filter_field_contain_list = [
        ("topic_name",),
    ]
