from django.shortcuts import render,redirect
from .models import Account,AccountForm
from django.contrib.auth.models import User
from patients.models import Patient
from django.contrib.auth import login,logout
from django.contrib import messages
# Create your views here.

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(email=email) 
        print(users)
        if users.exists():
            user = users.first()  
            if user.check_password(password):   
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        else:
            messages.error(request, 'User with this email does not exist.')
    return render(request, 'accounts/login.html')

def register(request):
    return render(request, 'accounts/register.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

# def showProfile(request):
#     return render(request, 'accounts/profile.html')

def showAllUsers(request):
    users = User.objects.all()
    users = {'users': users}
    return render(request, 'accounts/showUsers.html',users)

def registerUser(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # Use email as the username
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            Patient.objects.create(user=user, pesel=form.cleaned_data['pesel'])
            # Log the user in
            login(request, user)
            return redirect('accounts:showAllUsers')
    else:
        form = AccountForm()
    return render(request, 'accounts/register.html', {'form': form})