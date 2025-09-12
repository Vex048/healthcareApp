from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"
router = DefaultRouter()
router.register(r"profile", views.AccountViewSet, basename="account")
router.register(r"user", views.UserViewSet, basename="user")

app_name = "accounts"

urlpatterns = [
    path("", include(router.urls)),
]
