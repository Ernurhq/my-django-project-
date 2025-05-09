from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message, Profile

# Выбор роли
ROLE_CHOICES = [
    ('applicant', 'Соискатель'),
    ('company', 'Предприятие'),
]

# ✅ Регистрация
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Профиль создаётся отдельно при регистрации (в views)
        return user

# ✅ Форма сообщения
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['full_name', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваше сообщение'}),
        }

# ✅ Форма редактирования профиля
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=30, required=False, label="Фамилия")
    email = forms.EmailField(required=False, label="Email")
    photo = forms.ImageField(required=False, label="Фото профиля")

    class Meta:
        model = Profile
        fields = ['role']
