from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .seralizers import PostListSerializer, PostSerializer

from .models import Post


class PostViewSet(ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_class(self):
        return PostListSerializer if self.action == "list" else PostSerializer
