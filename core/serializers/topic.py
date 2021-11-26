from core.models.topic import Topic
from investhubapi.utils.serializer import CModelSerializer


class TopicSerializer(CModelSerializer):
    class Meta:
        model = Topic
        fields = ('id',
                  'topic_name')
