from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ChatBotMessage

@login_required
def chatbot_view(request):
    chatbot_messages = ChatBotMessage.objects.filter(user=request.user).order_by('timestamp')
    context = {"chatbot_messages":chatbot_messages}
    print("jol")
    # Ten and jest do AJAX -request
    if request.method == "POST":
        message = request.POST.get('message')
        print("Tesst")
        ChatBotMessage.objects.create(user=request.user,message=message,if_bot=False)
        print("test")
        reply = send_message_to_chatbot(message)
        print("test")
        ChatBotMessage.objects.create(user=request.user,message=reply,if_bot=True)
        return JsonResponse({'reply': reply})
    return render(request, 'chatbot/chatbot.html',context)


def send_message_to_chatbot(message):
    data = {
        "question": message
    }
    url_chatbot = 'http://192.168.1.42/service'
    try:
        response = requests.post(url=url_chatbot,json=data)
        bot_reply = response.json().get('reply')
    except Exception as e:
        bot_reply = "Couldnt connect to cahtbot servcie"
        
    return bot_reply
    
