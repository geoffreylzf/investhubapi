from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    is_active = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                  'is_staff', 'is_superuser',
                  'is_author',)

    # Following code is not use if using social auth
    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data.get('password'))
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     if validated_data.get('password'):
    #         validated_data['password'] = make_password(validated_data.get('password'))
    #     else:
    #         validated_data.pop('password', None)
    #
    #     return super().update(instance, validated_data)
