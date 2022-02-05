from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.posts.models import Post


class UserMixin(object):
    @staticmethod
    def _create_user(user_number: int):
        user = User.objects.create(
            username=f"test{user_number}",
            first_name=f"Name{user_number}",
            last_name=f"Lname{user_number}",
            email=f"test{user_number}@example.com",
        )
        user.set_password(f"testPassword")
        user.save()
        return user


class PostTestCase(APITestCase, UserMixin):
    def setUp(self) -> None:
        self.user_1 = self._create_user(user_number=1)
        self.user_2 = self._create_user(user_number=2)
        self.user_3 = self._create_user(user_number=3)
        self.user_4 = self._create_user(user_number=4)
        self.user_5 = self._create_user(user_number=5)

        self.login_url = reverse("auth:login")
        self.post_create_url = reverse("posts:post-create")
        self.post_list_url = reverse("posts:post-list")
        self.post_detail_url = reverse("posts:post-detail", kwargs={"pk": 1})
        self.post_like_url = reverse("posts:post-likes", kwargs={"pk": 1})


        self.post_1 = Post.objects.create(
            title="test title", body="Very interesting post"
        )

    def _get_user_token(self, username="test", password="testPassword"):
        response = self.client.post(
            self.login_url,
            {"username": username, "password": password},
            format="json",
        )
        response_data = response.json()
        return "JWT {}".format(response_data.get("token", ""))

    def test_create_post(self):
        """[Test creation post]"""

        result = self.client.post(
            self.post_list_url,
            {"title": "test title",
             "body": "Some interesting post"},
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_1.username),
        )
        self.assertEqual(result.status_code, 201)

        result = self.client.post(
            self.post_list_url,
            {"title": "test title",
             "body": "Some interesting post"},
        )
        self.assertEqual(result.status_code, 401)


    def test_list_threads(self):
        """[Test getting list of posts]"""

        result = self.client.get(self.post_list_url)
        self.assertEqual(result.status_code, 401)

        result = self.client.get(
            self.post_list_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_1.username),
        )
        self.assertEqual(result.status_code, 200)

        data = result.json()

        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]["id"], 1)

        self.assertTrue(data[0]["body"])

        self.assertEqual(data[0]["body"].get("body"), "Very interesting post")

        self.assertEqual(data[0]["likes_count"], 0)


    def test_update_post(self):

        result = self.client.patch(
            self.post_detail_url, HTTP_AUTHORIZATION=self._get_user_token()
        )
        self.assertEqual(result.status_code, 401)

        result = self.client.patch(
            self.post_detail_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_1.username),
        )
        self.assertEqual(result.status_code, 200)

        result = self.client.patch(
            self.post_detail_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_2.username),
        )
        self.assertEqual(result.status_code, 200)
        result = self.client.get(
            self.post_detail_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_1.username),
        )
        data = result.json()

        self.assertEqual(len(data), 0)

    def test_detail_thread(self):

        result = self.client.get(
            self.post_detail_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_1.username),
        )
        self.assertEqual(result.status_code, 200)

        result = self.client.get(
            self.post_detail_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=self.user_3.username),
        )
        self.assertEqual(result.status_code, 404)

        result = self.client.get(
            self.post_detail_url, HTTP_AUTHORIZATION=self._get_user_token()
        )
        self.assertEqual(result.status_code, 401)
