from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterForm, MessageForm, EditProfileForm
from .models import Profile, Message
# from .models import Article — Удалено

def some_view(request):
    from .models import Resume
    # использование Resume

# 🔹 Регистрация
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Пользователь уже существует!"})

        user = User.objects.create_user(username=username, email=email, password=password)

        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user, role=role)

        return redirect("login")

    return render(request, "users/register.html")

# 🔹 Вход
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

# 🔹 Выход
def logout_view(request):
    logout(request)
    return redirect('login')

# 🔹 Главная
@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.user = request.user
            message.save()
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'users/home.html', {'form': form})

# 🔹 Создание резюме
@login_required
def resume(request):
    return render(request, 'users/resume.html')

# 🔹 Профиль пользователя
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    resumes = []  # пока Resume не реализована
    favorites = []  # убрали Article
    return render(request, 'users/profile.html', {
        'profile': profile,
        'resumes': resumes,
        'favorites': favorites,
    })

# 🔹 Редактирование профиля
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            messages.success(request, "Профиль обновлён!")
            return redirect('profile')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = EditProfileForm(instance=profile, initial=initial_data)

    return render(request, 'users/edit_profile.html', {
        'form': form
    })
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def download_resume_pdf(request):
    profile = request.user.profile
    template = get_template("users/pdf_resume.html")
    html = template.render({"profile": profile})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Ошибка генерации PDF", status=500)
    return response
