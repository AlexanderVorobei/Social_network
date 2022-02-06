from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import create_user_account
from .serializers import (
    UserLoginSerializer,
    UserRegisterSerializer,
    PasswordChangeSerializer,
    AuthUserSerializer,
    EmptySerializer,
)


class AuthViewSet(viewsets.GenericViewSet, TokenObtainPairView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        "login": UserLoginSerializer,
        "register": UserRegisterSerializer,
        "password_change": PasswordChangeSerializer,
    }

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def logout(self, request):
        logout(request)
        data = {"success": "Successfully logged out"}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
