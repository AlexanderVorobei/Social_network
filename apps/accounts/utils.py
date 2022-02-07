from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_account(
    username: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    **extra_fields
):
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **extra_fields
    )
    return user
