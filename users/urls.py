from django.urls import path
from .views import register, login_view, logout_view, profile, home, resume
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('', home, name='home'),
    path('resume/', resume, name='resume')
]
