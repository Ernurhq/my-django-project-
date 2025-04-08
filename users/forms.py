from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('applicant', 'Соискатель'),
    ('company', 'Предприятие'),
]

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)  # Добавляем выбор роли

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.profile.role = self.cleaned_data["role"]  # Сохраняем роль
        if commit:
            user.save()
            user.profile.save()  # Сохраняем профиль
        return user

from .models import Message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['full_name', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваше сообщение'}),
        }