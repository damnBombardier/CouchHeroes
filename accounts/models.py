# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    """
    Расширенный профиль игрока.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Можно добавить аватар, биографию и т.д.
    achievements = models.ManyToManyField('Achievement', blank=True) # Создать модель Achievement
    premium_status = models.BooleanField(default=False) # Для "Божественного пакета"
    
    # Статистика игрока
    total_heroes = models.PositiveIntegerField(default=1) # Или список героев, если их может быть много
    games_played = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

# Модель для достижений
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True) # Путь к иконке или символьный код
    
    def __str__(self):
        return self.name

# Сигналы Django для автоматического создания профиля при регистрации пользователя
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PlayerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.playerprofile.save()
