from rest_framework import serializers
from .models import Post


class GetUserMixin:
    """
    Get user from request
    """

    def get_user_from_request(self):
        return getattr(self.context.get("request"), "user", None)


class PostSerializer(GetUserMixin, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(
        many=True, required=False, read_only=True
    )
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "body",
            "likes",
            "likes_count",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()

    def create(self, validated_data):
        user = self.get_user_from_request()
        validated_data.update(user=user)
        post = super().create(validated_data=validated_data)
        return post

    def update(self, instance, validated_data):
        if instance.user != self.get_user_from_request():
            raise serializers.ValidationError("Your can't edit this post")
        title_data = validated_data.pop("title", "")
        body_data = validated_data.pop("body", "")
        if not title_data and not body_data:
            return instance
        if title_data:
            instance.title = title_data
        if body_data:
            instance.body = body_data
        post = super().update(instance=instance, validated_data=validated_data)
        return post

    def destroy(self, instance):
        if instance.user != self.get_user_from_request():
            raise serializers.ValidationError("Your can't delete this post")
        else:
            instance.delete()
            return None


class PostListSerializer(GetUserMixin, serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "body",
            "likes",
            "likes_count",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class PostLikeSerializer(GetUserMixin, serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(
        many=True, required=False, read_only=True
    )
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "likes",
            "likes_count",
        )

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()

    def update(self, instance, validated_data):
        if not self.get_user_from_request():
            raise serializers.ValidationError("Your can't like this post")
        likes_for_update = self.get_user_from_request()
        if likes_for_update in instance.likes.all():
            instance.likes.remove(likes_for_update)
        else:
            instance.likes.add(likes_for_update)
        return instance
