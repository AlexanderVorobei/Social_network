from rest_framework.routers import DefaultRouter

from .views import AuthViewSet

app_name = "accounts"
router = DefaultRouter(trailing_slash=False)
router.register("", AuthViewSet, basename="auth")

urlpatterns = [] + router.urls
