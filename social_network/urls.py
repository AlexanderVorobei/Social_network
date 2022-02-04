"""social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import debug_toolbar
from rest_framework_swagger.views import get_swagger_view
from .settings import DEBUG

schema_view = get_swagger_view(title='Social Network API')

urlpatterns = [
    path("api/v1/post/", include("apps.posts.urls", namespace="posts")),
    path("api/v1/auth/", include("apps.accounts.urls", namespace="auth")),
    path("docs", schema_view),
]

if DEBUG:
    urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))
