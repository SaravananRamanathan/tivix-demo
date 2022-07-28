from rest_framework import serializers
from userAccess.models import CustomUser


class customUserSerializer(serializers.ModelSerializer):
    ""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # hashing password.
        instance.save()
        return instance
