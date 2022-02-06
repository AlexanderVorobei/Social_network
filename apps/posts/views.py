from rest_framework.permissions import IsAuthenticated
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

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PostSerializer
    serializer_classes = {
        "list": PostListSerializer,
        "likes": PostLikeSerializer,
    }

    @action(
        methods=[
            "PATCH",
        ],
        url_path="(?P<pk>[^/.]+)/likes",
        detail=False,
    )
    def likes(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
