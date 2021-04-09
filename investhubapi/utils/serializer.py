
from rest_framework import serializers


class CModelSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_by = serializers.ReadOnlyField(source="updated_by.username")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', None)
        fields = None
        exclude_fields = None
        if context is not None:
            fields = context.pop('fields', None)
            exclude_fields = context.pop('exclude_fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)