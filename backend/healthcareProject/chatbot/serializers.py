from rest_framework import serializers
from .models import ChatBotMessage


class ChatBotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotMessage
        fields = ["id", "user", "message", "response", "timestamp", "if_bot"]
        read_only_fields = ["user", "response", "timestamp", "if_bot"]


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)


class ChatResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    timestamp = serializers.DateTimeField()
