from django.db import models
from django.contrib.auth.models import User
from heroes.models import Hero

class Quest(models.Model):
    """
    Модель квеста/задания.
    """
    # Типы квестов
    QUEST_TYPES = [
        ('system', 'Системный'),
        ('user_generated', 'Пользовательский'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    quest_type = models.CharField(max_length=20, choices=QUEST_TYPES, default='system', verbose_name="Тип")
    
    # Требования для начала квеста (уровень, предметы и т.д.)
    required_level = models.PositiveIntegerField(default=1, verbose_name="Требуемый уровень")
    # required_items = models.ManyToManyField('Item', blank=True, verbose_name="Требуемые предметы") # Позже
    
    # Награды за выполнение
    reward_experience = models.PositiveIntegerField(default=50, verbose_name="Награда в опыте")
    reward_gold = models.PositiveIntegerField(default=20, verbose_name="Награда в золоте")
    # reward_items = models.ManyToManyField('Item', blank=True, through='QuestRewardItem', verbose_name="Награды предметами") # Позже
    
    # Создатель (для пользовательских квестов)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_quests', verbose_name="Создатель")
    
    # Модерация пользовательских квестов
    is_approved = models.BooleanField(default=False, verbose_name="Одобрен")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_quests', verbose_name="Кем одобрен")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class HeroQuest(models.Model):
    """
    Связь между героем и квестом (прогресс выполнения).
    """
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='quests')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    
    # Статус выполнения
    STATUS_CHOICES = [
        ('not_started', 'Не начат'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнен'),
        ('failed', 'Провален'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name="Статус")
    
    # Прогресс (если квест состоит из нескольких этапов)
    progress = models.PositiveIntegerField(default=0, verbose_name="Прогресс")
    # max_progress = models.PositiveIntegerField(default=1, verbose_name="Максимальный прогресс") # Для сложных квестов
    
    # Дата начала и завершения
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата начала")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hero', 'quest') # Герой не может иметь несколько записей для одного квеста
        verbose_name = "Квест героя"
        verbose_name_plural = "Квесты героев"

    def __str__(self):
        return f"{self.hero.name} - {self.quest.title} ({self.get_status_display()})"

# TODO: Модели для Event, InventoryItem будут добавлены позже.

