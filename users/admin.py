from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Создаем inline для редактирования профиля в админке
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'

# Расширяем стандартную админку пользователей
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    # Добавляем поле "role" в список пользователей
    def role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'Не указано'
    role.short_description = 'Роль'

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('profile__role', 'is_staff', 'is_active')

# Перерегистрируем модель User с нашим новым админ-классом
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)


from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'created_at')  # Отображаемые поля в админке
    search_fields = ('full_name', 'message')  # Поиск по имени и сообщению
    list_filter = ('created_at',)  # Фильтр по дате
