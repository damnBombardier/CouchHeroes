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

class Item(models.Model):
    """
    Модель игрового предмета.
    """
    ITEM_TYPES = [
        ('healing', 'Лечащий'),
        ('weapon', 'Оружие'),
        ('armor', 'Доспех'),
        ('artifact', 'Артефакт'),
        ('quest', 'Квестовый'),
        ('junk', 'Хлам'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, verbose_name="Тип предмета")
    
    # Свойства предмета (для экипировки)
    power = models.IntegerField(default=0, verbose_name="Сила") # Для оружия
    defense = models.IntegerField(default=0, verbose_name="Защита") # Для доспехов
    healing_amount = models.IntegerField(default=0, verbose_name="Лечебный эффект") # Для лечащих
    
    # Редкость
    RARITY_CHOICES = [
        ('common', 'Обычный'),
        ('uncommon', 'Необычный'),
        ('rare', 'Редкий'),
        ('epic', 'Эпический'),
        ('legendary', 'Легендарный'),
    ]
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common', verbose_name="Редкость")
    
    # Цена продажи (если применимо)
    sell_price = models.PositiveIntegerField(default=1, verbose_name="Цена продажи")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()})"

class Inventory(models.Model):
    """
    Связь между героем и предметом в его инвентаре.
    """
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='inventory_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    
    acquired_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hero', 'item') # Уникальность предмета в инвентаре героя
        verbose_name = "Предмет в инвентаре"
        verbose_name_plural = "Предметы в инвентаре"

    def __str__(self):
        return f"{self.hero.name} - {self.item.name} (x{self.quantity})"

    def use_item(self):
        """
        Использует один экземпляр предмета, применяя его эффект к герою.
        Возвращает сообщение о результате.
        """
        if self.quantity <= 0:
            return f"У {self.hero.name} нет {self.item.name} в инвентаре."

        if self.item.item_type == 'healing':
            if self.hero.health >= self.hero.max_health:
                return f"{self.hero.name} полностью здоров и не нуждается в лечении."
            
            heal_amount = self.item.healing_amount
            self.hero.health = min(self.hero.max_health, self.hero.health + heal_amount)
            self.hero.save()
            
            self.quantity -= 1
            if self.quantity <= 0:
                self.delete() # Удаляем запись, если предметы закончились
            else:
                self.save()
            
            return f"{self.hero.name} использует {self.item.name} и восстанавливает {heal_amount} здоровья. Здоровье: {self.hero.health}/{self.hero.max_health}."
        
        elif self.item.item_type in ['weapon', 'armor', 'artifact', 'quest', 'junk']:
            return f"{self.item.name} нельзя использовать таким образом. Попробуйте 'Экипировать'."
        
        else:
            return f"Неизвестный тип предмета для использования: {self.item.item_type}."

class Equipment(models.Model):
    """
    Экипировка героя.
    """
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE, related_name='equipment')
    
    # Слоты экипировки
    weapon = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipped_as_weapon')
    armor = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipped_as_armor')
    # Можно добавить другие слоты: амулет, кольцо и т.д.
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Экипировка"
        verbose_name_plural = "Экипировки"

    def __str__(self):
        return f"Экипировка {self.hero.name}"

    def get_total_power(self):
        """Возвращает общую силу от экипировки."""
        total = 0
        if self.weapon:
            total += self.weapon.power
        # if self.armor: # Если будет свойство power у брони
        #     total += self.armor.power
        return total

    def get_total_defense(self):
        """Возвращает общую защиту от экипировки."""
        total = 0
        # if self.weapon: # Если будет свойство defense у оружия
        #     total += self.weapon.defense
        if self.armor:
            total += self.armor.defense
        return total

    def equip_item(self, item: Item):
        """
        Экипирует предмет, заменяя текущий в слоте, если он есть.
        Возвращает сообщение о результате.
        """
        if item.item_type == 'weapon':
            old_item = self.weapon
            self.weapon = item
            self.save()
            if old_item:
                return f"{self.hero.name} экипирует {item.name}, снимая {old_item.name}."
            else:
                return f"{self.hero.name} экипирует {item.name}."
        elif item.item_type == 'armor':
            old_item = self.armor
            self.armor = item
            self.save()
            if old_item:
                return f"{self.hero.name} надевает {item.name}, снимая {old_item.name}."
            else:
                return f"{self.hero.name} надевает {item.name}."
        else:
            return f"{item.name} нельзя экипировать."

    def unequip_item(self, item_type: str):
        """
        Снимает предмет из указанного слота.
        item_type: 'weapon' или 'armor'.
        Возвращает сообщение о результате.
        """
        if item_type == 'weapon' and self.weapon:
            removed_item = self.weapon
            self.weapon = None
            self.save()
            return f"{self.hero.name} снимает {removed_item.name}."
        elif item_type == 'armor' and self.armor:
            removed_item = self.armor
            self.armor = None
            self.save()
            return f"{self.hero.name} снимает {removed_item.name}."
        else:
            return f"В слоте {item_type} ничего не надето."

# Сигналы для автоматического создания Equipment при создании героя
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Hero)
def create_hero_equipment(sender, instance, created, **kwargs):
    if created:
        Equipment.objects.create(hero=instance)
