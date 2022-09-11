"""
Serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    """
    Serializers for the user object.
    """

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "full_name"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "full_name": {"min_length": 5},
        }

    def create(self, validated_data):
        """
        create and return a user with encryted password
        """
        print('----miraaaa serializer----')
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return user.
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user auth token.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = get_user_model().objects.filter(email=email)
        print(user)
        if len(user) == 0:
            msg = _('this email not exist in our database.')
            raise serializers.ValidationError(msg, code='authorization')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

