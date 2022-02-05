from rest_framework import serializers
from .models import Post


class GetUserMixin:

    def get_user_from_request(self):
        return getattr(self.context.get("request"), "user", None)


class PostSerializer(GetUserMixin, serializers.ModelSerializer):
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
    likes = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
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

    def get_likes(self, obj):
        if self.get_user_from_request() not in obj.likes:
            obj.likes.add(self.get_user_from_request())
        else:
            obj.likes.remove(self.get_user_from_request())
            obj.save()
        return obj.likes

    def update(self, instance, validated_data):
        if not self.get_user_from_request():
            raise serializers.ValidationError("Your can't like this post")
        likes_for_update = self.get_user_from_request()
        if likes_for_update in instance.likes.all():
            instance.likes.remove(likes_for_update)
        else:
            instance.likes.add(likes_for_update)
        return instance
