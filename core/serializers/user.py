from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name', 'last_name',
                  'password',
                  'date_joined',
                  'is_active',
                  'is_staff', 'is_superuser',
                  'is_merchant_user',
                  'is_customer',)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data.get('password'))
        else:
            validated_data.pop('password', None)

        return super().update(instance, validated_data)
