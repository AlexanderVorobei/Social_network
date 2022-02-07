from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from .utils import create_user_account
from .serializers import (
    UserRegisterSerializer,
    AuthUserSerializer,
)

User = get_user_model()


class AuthViewSet(GenericViewSet, TokenViewBase, UpdateModelMixin):
    """
    A viewset that provides `login()`, `login_refresh()`, `register()`
    and `password_change()` actions.
    """

    permission_classes = [AllowAny]
    serializer_classes = {
        "login": TokenObtainPairSerializer,
        "login_refresh": TokenRefreshSerializer,
        "register": UserRegisterSerializer,
    }

    @action(methods=["POST"], detail=False)
    def login(self, request):
        return super().post(request)

    @action(methods=["POST"], url_path="login/refresh", detail=False)
    def login_refresh(self, request):
        return super().post(request)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
