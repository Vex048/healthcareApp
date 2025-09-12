from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"history", views.ChatBotMessageViewSet, basename="chatbot-history")

app_name = "chatbot"

urlpatterns = [
    path("", include(router.urls)),
    path("send/", views.ChatbotAPIView.as_view(), name="chatbot-send"),
]
