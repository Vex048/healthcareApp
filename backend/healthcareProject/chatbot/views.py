from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import ChatBotMessage
from .serializers import (
    ChatBotMessageSerializer,
    ChatRequestSerializer,
    ChatResponseSerializer,
)


class ChatBotMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatBotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own chat history
        return ChatBotMessage.objects.filter(user=self.request.user).order_by(
            "-timestamp"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatbotAPIView(APIView):
    """API endpoint for interacting with the chatbot."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data["message"]

            # Process message with chatbot
            from .views import send_message_to_chatbot

            response = send_message_to_chatbot(message)

            # Save the interaction
            chat_message = ChatBotMessage.objects.create(
                user=request.user, message=message, response=response, if_bot=False
            )

            response_data = {"message": response, "timestamp": chat_message.timestamp}

            return Response(
                ChatResponseSerializer(response_data).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
