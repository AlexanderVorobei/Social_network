from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager


User = get_user_model()


class UserLoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super(UserLoginSerializer, cls).get_token(user)
        token["username"] = user.username

        return token


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
        )
        read_only_fields = ("id", "is_active", "is_staff")


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("current_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Current password does not match")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class EmptySerializer(serializers.Serializer):
    pass
