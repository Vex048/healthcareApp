from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('showAllUsers/', views.showAllUsers, name='showAllUsers'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.showProfile, name='profile'),
]