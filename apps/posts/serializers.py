from rest_framework import serializers
from .models import Post


class GetUserMixin:
    """[summary]
    """
    def get_user_from_request(self):
        return getattr(self.context.get("request"), "user", None)


class PostSerializer(GetUserMixin, serializers.ModelSerializer):
    """[summary]

    Args:
        GetUserMixin ([type]): [description]
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "body",
            "likes",
            "likes_count"
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
        if not (title_data | body_data):
            return instance
        instance.title = title_data
        instance.body = body_data
        return instance

    def destroy(self, instance):
        if instance.user != self.get_user_from_request():
            raise serializers.ValidationError("Your can't delete this post")
        else:
            instance.delete()
            return instance

    def validate_user(self, value):
        user = self.get_user_from_request()
        if not user:
            raise serializers.ValidationError("Can't find user.")
        if not self.instance:
            if user not in value:
                raise serializers.ValidationError("Current user must be author. ")
        return value


class PostListSerializer(GetUserMixin, serializers.ModelSerializer):
    """[summary]

    Args:
        GetUserMixin ([type]): [description]
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
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
        )

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class PostLikeSerializer(GetUserMixin, serializers.ModelSerializer):
    """[summary]

    Args:
        GetUserMixin ([type]): [description]
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    likes = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
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

    def likes(self, instance):
        like_for_change = self.get_user_from_request()
        if not like_for_change:
            raise serializers.ValidationError("Not found.")
        if like_for_change in instance.likes:
            instance.likes.remove(like_for_change)
        else:
            instance.likes.add(like_for_change)
        return instance
