from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .serializers import PostListSerializer, PostSerializer, PostLikeSerializer
from .models import Post


class PostViewSet(ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]

    @action(methods=['POST', ], detail=False)
    def likes(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.partial_update(serializer.validated_data['likes'])

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "likes":
            return PostLikeSerializer
        else:
            return PostSerializer