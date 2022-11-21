import re

import django.contrib.auth.password_validation as validators
from api.models import Follow
from django.core import exceptions
from rest_framework import serializers
from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя.
    """
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        regex = re.compile('^[A-Za-z0-9_.@+-]+$')
        if not regex.search(value):
            raise serializers.ValidationError(
                'Адрес электронной почты содержит недопустимые символы')
        return value

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(CreateUserSerializer, self).validate(data)


class ShowUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения пользователя.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonyous
            and Follow.objects.filter(user=user, author=obj).exists()
        )
