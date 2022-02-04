from rest_framework import serializers
from django.contrib.auth import get_user_model


def create_user_account(username, password, first_name="", last_name="", **extra_fields):
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **extra_fields
    )
    return user
