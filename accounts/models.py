# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class PlayerProfile(models.Model):
    """
    Расширенный профиль игрока.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Можно добавить аватар, биографию и т.д.
    achievements = models.ManyToManyField('Achievement', blank=True, related_name='players')
    premium_status = models.BooleanField(default=False, verbose_name="Премиум статус") # Для "Божественного пакета"
    bio = models.TextField(blank=True, verbose_name="Биография")
    
    # Статистика игрока
    total_heroes = models.PositiveIntegerField(default=1, verbose_name="Всего героев")
    games_played = models.PositiveIntegerField(default=0, verbose_name="Игр сыграно")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.username})

class Achievement(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=100, blank=True, verbose_name="Иконка") # Путь к иконке или символьный код
    points = models.PositiveIntegerField(default=10, verbose_name="Очки достижения")
    
    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
    
    def __str__(self):
        return self.name

class Notification(models.Model):
    """
    Модель уведомления для пользователя.
    """
    NOTIFICATION_TYPES = [
        ('info', 'Информация'),
        ('success', 'Успех'),
        ('warning', 'Предупреждение'),
        ('danger', 'Ошибка'), # Или критическое событие
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Получатель")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    message = models.TextField(verbose_name="Сообщение")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info', verbose_name="Тип")
    
    # Ссылка на объект, связанный с уведомлением (например, герой, квест)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    # object_id = models.PositiveIntegerField(null=True, blank=True)
    # content_object = GenericForeignKey('content_type', 'object_id')
    # Пока используем простую текстовую ссылку
    link = models.URLField(blank=True, null=True, verbose_name="Ссылка")
    
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']

    def __str__(self):
        return f"Уведомление для {self.recipient.username}: {self.title}"

    def mark_as_read(self):
        """Помечает уведомление как прочитанное."""
        if not self.is_read:
            self.is_read = True
            self.save()

# Сигналы Django для автоматического создания профиля при регистрации пользователя
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PlayerProfile.objects.create(user=instance)

# Этот сигнал может вызвать проблемы при массовых операциях, 
# лучше использовать try/except в коде, где это нужно.
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()
