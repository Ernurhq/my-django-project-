from django.urls import path
from .views import register, login_view, logout_view, profile, home, resume
from django.contrib.auth import views as auth_views
from . import views
from .views import download_resume_pdf, profile, resume, register, login_view, logout_view, home, edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('resume/', resume, name='resume'),
    path('resume/download/', download_resume_pdf, name='download_resume'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]