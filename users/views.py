from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from users.forms import UserCreationForm
from users.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]  # Получаем роль из формы

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Пользователь уже существует!"})

        user = User.objects.create_user(username=username, email=email, password=password)

        # 🔹 Проверяем, есть ли уже профиль для этого пользователя
        if not hasattr(user, 'profile'):  # <-- Исправление
            Profile.objects.create(user=user, role=role)

        return redirect("login")  # Перенаправляем на страницу входа

    return render(request, "users/register.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Неверные данные'})
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required(login_url='login')  # Перенаправление на страницу входа
def home(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.user = request.user  # Если пользователь авторизован, добавляем его
            message.save()
            return redirect('home')  # Обновляем страницу после отправки
    else:
        form = MessageForm()
    
    return render(request, 'users/home.html', {'form': form})


def resume(request):
    return render(request, 'users/resume.html')
