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
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # Use email as the username
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            Patient.objects.create(user=user, pesel=form.cleaned_data['pesel'])
            login(request, user)
            return redirect('accounts:showAllUsers')
    else:
        form = AccountForm()
    return render(request, 'accounts/register.html', {'form': form})





from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

def test_password(request, username):
    """Temporary debugging function - REMOVE AFTER TESTING"""
    try:
        user = User.objects.get(username=username)
        
        result = None
        if request.method == 'POST':
            password = request.POST.get('password')
            if check_password(password, user.password):
                result = f"Password '{password}' is CORRECT for user {username}"
            else:
                result = f"Password '{password}' is INCORRECT for user {username}"
        
        return render(request, 'accounts/test_password.html', {
            'username': username,
            'result': result
        })
    except User.DoesNotExist:
        return HttpResponse(f"User {username} not found", status=404)
    
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class DebugPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def form_valid(self, form):
        # Print debug info
        print("=" * 50)
        print("PASSWORD RESET FORM VALID")
        print(f"User: {self.user.username}")
        print(f"New password length: {len(form.cleaned_data['new_password1'])}")
        print("=" * 50)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Override form_invalid to see validation errors"""
        print("=" * 50)
        print("PASSWORD RESET FORM INVALID")
        print(f"Errors: {form.errors}")
        print("=" * 50)
        return super().form_invalid(form)