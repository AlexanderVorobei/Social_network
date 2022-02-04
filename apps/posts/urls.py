from rest_framework.routers import DefaultRouter

from .views import PostViewSet

app_name = "posts"
router = DefaultRouter(trailing_slash=False)
router.register("", PostViewSet, basename="posts")

urlpatterns = [] + router.urls
