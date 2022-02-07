from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action
from rest_framework import viewsets

from .serializers import (
    PostListSerializer,
    PostSerializer,
    PostLikeSerializer,
)
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()`,  `list()` and `likes()` actions.
    """

    serializer_class = PostSerializer
    serializer_classes = {
        "list": PostListSerializer,
        "likes": PostLikeSerializer,
    }

    @action(methods=["PATCH"], url_path="(?P<pk>[^/.]+)/likes", detail=False)
    def likes(self, request, *args, **kwargs):
        """
        Update a model instance - add or remove like from user.
        """
        return super().partial_update(request, *args, **kwargs)

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.
        """
        return Post.objects.all()

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "read"]:
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]
