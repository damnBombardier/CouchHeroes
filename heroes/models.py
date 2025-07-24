# heroes/models.py
from django.db import models
from django.contrib.auth.models import User
import random

class Hero(models.Model):
    """
    Модель героя-почитателя.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Имя героя")
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hero')
    
    # Атрибуты героя
    level = models.PositiveIntegerField(default=1)
    health = models.PositiveIntegerField(default=100)
    max_health = models.PositiveIntegerField(default=100)
    gold = models.PositiveIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)
    
    # Инвентарь, гильдия, другие состояния - добавить позже
    
    # Состояния героя (автоматическое поведение)
    STATE_CHOICES = [
        ('adventure', 'Приключение'),
        ('fight', 'Бой'),
        ('quest', 'Квест'),
        ('rest', 'Отдых'),
        # ... другие состояния ...
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='adventure')
    
    # Координаты или локация - упрощенно
    location = models.CharField(max_length=100, default="Город")
    
    # Время последнего обновления состояния героя (для ZPG engine)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Статистика
    monsters_killed = models.PositiveIntegerField(default=0)
    quests_completed = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (уровень {self.level})"

    def get_random_action(self):
        """
        Возвращает случайное действие героя (для демонстрации ZPG).
        В реальном движке это будет сложнее.
        """
        actions = [
            f"{self.name} идет по тропе.",
            f"{self.name} осматривает окрестности.",
            f"{self.name} находит немного золота!",
            f"{self.name} сталкивается с монстром!",
            f"{self.name} отдыхает у костра.",
            f"{self.name} слышит странный шепот...",
        ]
        return random.choice(actions)

    def apply_lightning_strike(self):
        """Логика удара молнии."""
        # Пример: останавливает действие или наносит урон
        self.health = max(0, self.health - 10) # Пример урона
        self.save()
        return f"Молния ударила {self.name}! Здоровье: {self.health}/{self.max_health}"

    def apply_divine_speech(self, message):
        """Логика божественной реплики."""
        # Пример: увеличивает опыт или здоровье
        self.experience += 5
        self.health = min(self.max_health, self.health + 5)
        self.save()
        return f"{self.name} услышал: '{message}'. Получено 5 опыта и 5 здоровья!"

# Дополнительные модели для событий, инвентаря и т.д. будут добавлены позже.
