from rest_framework import serializers
from .models import Post


class GetUserMixin:
    def get_user_from_request(self):
        return getattr(self.context.get("request"), "user", None)


class PostSerializer(GetUserMixin, serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "body",
        )
    def create(self, validated_data):
        user = self.get_user_from_request()
        validated_data.update(user=user)
        post = super().create(validated_data=validated_data)
        return post

    def update(self, instance, validated_data):
        if instance.sender != self.get_user_from_request():
            raise serializers.ValidationError("Your can't edit this message")
        text_data = validated_data.pop("text", "")
        if not text_data:
            return instance
        instance.text = text_data
        return instance

    def destroy(self, instance):
        if instance.sender != self.get_user_from_request():
            raise serializers.ValidationError("Your can't delete this message")
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
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "body",
            "likes",
        )
