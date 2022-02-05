from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

from .serializers import PostListSerializer, PostSerializer, PostLikeSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    """[summary]

    Args:
        ModelViewSet ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = [
        IsAuthenticated,
    ]

    @action(methods=['PATCH', ], url_path="(?P<pk>[^/.]+)/likes", detail=False)
    def likes(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "likes":
            return PostLikeSerializer
        else:
            return PostSerializer
