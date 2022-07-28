from dataclasses import fields
from rest_framework import serializers
from userAccess.models import CustomUser
from .models import Budget, Item, share


class shareSerializer(serializers.ModelSerializer):
    ""
    class Meta:
        ""
        model = share
        fields = '__all__'


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


class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class budgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
