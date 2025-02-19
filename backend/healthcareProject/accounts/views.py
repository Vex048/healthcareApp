from django.shortcuts import render
from .models import Account
# Create your views here.

def login(request):
    return render(request, 'accounts/login.html')

def register(request):
    return render(request, 'accounts/register.html')


def showUsers(request):
    users = Account.objects.all()
    users = {'users': users}
    return render(request, 'accounts/showUsers.html',users)