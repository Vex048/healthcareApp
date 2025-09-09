from django.shortcuts import render

# Create your views here.
from huggingface_hub import login
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
from .models import ChatBotMessage
import re

chatbot = None

from transformers import AutoModelForCausalLM, AutoTokenizer,pipeline

def initialize_chatbot():
    """Initialize the chatbot pipeline once"""
    global chatbot
    if chatbot is None:
        try:
            print("Loading chatbot model...")
            model_name = "Vex048/medical-chatbot-full-not-quantizied"
            token = os.getenv('HUGGINGFACE_TOKEN')
            if token:
                login(token=token)
                print("Logged in to Hugging Face")
            
            try:
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)

                chatbot = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    framework='pt',
                    device=-1  
                )
                print("Chatbot model loaded successfully")
            except Exception as specific_e:
                print(f"Error loading specific model: {specific_e}")
        except Exception as e:
            print(f"Error in initialize_chatbot: {e}")
            return None
    return chatbot

@login_required
def chatbot_view(request):
    chatbot_messages = ChatBotMessage.objects.filter(user=request.user).order_by('timestamp')
    context = {"chatbot_messages":chatbot_messages}
    print("jol")
    if request.method == "POST":
        message = request.POST.get('message')
        ChatBotMessage.objects.create(user=request.user,message=message,if_bot=False)
        reply = send_message_to_chatbot(message)
        ChatBotMessage.objects.create(user=request.user,message=reply,if_bot=True)
        return JsonResponse({'reply': reply})
    return render(request, 'chatbot/chatbot.html',context)


def trim_signature(text):
    signature_phrases = [
        r'hope this helps',
        r'hope that helps',
        r'hope my answer helps',
        r'take care',
        r'best regards',
        r'kind regards',
        r'regards',
        r'dr\.?\s+\w+(\s+\w+)*',  
    ]

    pattern = re.compile(r'(' + '|'.join(signature_phrases) + r')', re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return text[:match.start()].strip()
    return text.strip()

def send_message_to_chatbot(question):
    chatbot = initialize_chatbot()
    
    if chatbot is None:
        return "Couldn't initialize the chatbot model. Please try again later."
    
    try:
        system_instruction = (
            "You are a professional medical chatbot assistant providing helpful advice. "
            "Always respond as the medical professional, never as the patient. "
            "Be concise, accurate, and helpful. Do not include fake doctor names or credentials. "
            "Do not include contact information."
        )
        
        # Format the prompt with system instruction and patient question
        prompt = f"{system_instruction}\n\nPatient Question: {question}\n\nMedical Response:"
        
        # Generate response with specified parameters
        result = chatbot(
            prompt,
            min_length = 30,
            #max_length=128,          
            temperature=0.4,         
            top_p=0.9,              
            repetition_penalty=1.2,  
            num_return_sequences=1,   
            no_repeat_ngram_size=3,
        )
        
        # Extract the generated text
        generated_text = result[0]['generated_text']
        
        bot_reply = generated_text.replace(prompt, "").strip()
        trimmed_bot_reply = trim_signature(bot_reply)
            
        return trimmed_bot_reply
    except Exception as e:
        return f"Couldn't generate a response: {str(e)}"


