from rest_framework import fields
from rest_framework.serializers import Serializer
from apps.authentication.models import *


class BaseUserSerializer(Serializer):
    first_name = fields.CharField(max_length=30, required=True)
    last_name = fields.CharField(max_length=150, required=True)
    phone = fields.CharField(max_length=255)
    email = fields.EmailField(required=True)

    def create(self, validated_data):
        first_name = validated_data.get("first name", None)
        last_name = validated_data.get("last name", None)
        phone = validated_data.get("phone", None)
        email = validated_data.get("email", None)
        # validated_data.pop("first name", "last name", "phone", "email")

        return User.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email)

    def update(self, instance, validated_data):
        instance.new_first_name = validated_data.get('first name')
        instance.new_last_name = validated_data.get('last name')
        instance.new_phone = validated_data.get('phone')
        instance.new_email = validated_data.get('email')
        instance.save()
        user = instance.user
        user.save()
