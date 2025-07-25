# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PlayerProfile, Achievement, Notification

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

@admin.register(Notification) # Добавлено
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'title', 'message')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        """Действие администратора: пометить выбранные уведомления как прочитанные."""
        updated_count = queryset.update(is_read=True)
        self.message_user(request, f"{updated_count} уведомлений помечены как прочитанные.")
    mark_as_read.short_description = "Пометить выбранные как прочитанные"

