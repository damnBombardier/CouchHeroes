# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PlayerProfile, Achievement

# Определим инлайн для профиля, чтобы он отображался на странице пользователя
class PlayerProfileInline(admin.StackedInline):
    model = PlayerProfile
    can_delete = False
    verbose_name_plural = 'Профили игроков'

# Расширим стандартный UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (PlayerProfileInline,)

# Отменим регистрацию стандартного User и зарегистрируем наш расширенный
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Зарегистрируем модель Achievement
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ('name',)
