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
    guild_membership = models.OneToOneField('guilds.GuildMembership', on_delete=models.SET_NULL, null=True, blank=True, related_name='hero')
    # Связь с гильдией будет через GuildMembership
    # На самом деле, связь уже определена в GuildMembership как OneToOneField(hero)
    # Поэтому Hero автоматически получает related_name='guild_membership'

    # Атрибуты героя
    level = models.PositiveIntegerField(default=1)
    health = models.PositiveIntegerField(default=100)
    max_health = models.PositiveIntegerField(default=100)
    gold = models.PositiveIntegerField(default=10) # Начальное золото
    experience = models.PositiveIntegerField(default=0)
    
    # Инвентарь, гильдия, другие состояния - добавить позже
    
    # Состояния героя (автоматическое поведение)
    STATE_CHOICES = [
        ('adventure', 'Приключение'),
        ('fight', 'Бой'),
        ('quest', 'Квест'),
        ('rest', 'Отдых'),
        ('dead', 'Мертв'),
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
            f"{self.name} идет по тропе в поисках приключений.",
            f"{self.name} осматривает окрестности, оглядывая каждый куст.",
            f"{self.name} находит немного золота!",
            f"{self.name} сталкивается с монстром!",
            f"{self.name} отдыхает у костра, восстанавливая силы.",
            f"{self.name} слышит странный шепот из кустов...",
            f"{self.name} натыкается на древний артефакт!",
            f"{self.name} получает задание от таинственного незнакомца.",
            f"{self.name} участвует в гильдейском турнире.",
            f"{self.name} отправляется на рыбалку.",
            f"{self.name} изучает старинную карту.",
            f"{self.name} помогает крестьянину с урожаем.",
        ]
        return random.choice(actions)

    def apply_lightning_strike(self):
        """Логика удара молнии."""
        if self.state == 'dead':
            return f"{self.name} уже мертв. Молния пролетает мимо."
        # Пример: останавливает действие или наносит урон
        damage = 15 # Более сильный удар
        self.health = max(0, self.health - damage) # Пример урона
        self.save()
        if self.health == 0:
            self.state = 'dead'
            self.deaths += 1
            self.save()
            return f"Молния сокрушила {self.name}! Герой погиб."
        return f"Молния ударила {self.name}! Нанесено {damage} урона. Здоровье: {self.health}/{self.max_health}"

    def apply_divine_speech(self, message):
        """Логика божественной реплики."""
        if self.state == 'dead':
            return f"{self.name} мертв и не может услышать ваши слова."
        # Пример: увеличивает опыт или здоровье
        exp_gain = 7
        heal_amount = 8
        self.experience += exp_gain
        self.health = min(self.max_health, self.health + heal_amount)
        self.save()
        return f"{self.name} услышал: '{message}'. Получено {exp_gain} опыта и {heal_amount} здоровья!"

    @classmethod
    def create_for_user(cls, user):
        """Создает героя для нового пользователя."""
        hero_name = f"{user.username}'s Hero"
        # Можно добавить логику генерации уникального имени, если нужно
        hero = cls.objects.create(name=hero_name, owner=user)
        return hero

# Дополнительные модели для событий, инвентаря и т.д. будут добавлены позже.
