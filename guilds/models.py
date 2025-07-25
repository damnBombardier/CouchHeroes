# guilds/models.py (новый файл)
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone # Добавлено
import uuid
from heroes.models import Hero

class Guild(models.Model):
    """
    Модель гильдии.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-имя") # Для ЧПУ
    description = models.TextField(blank=True, verbose_name="Описание")
    motto = models.CharField(max_length=200, blank=True, verbose_name="Девиз")
    
    # Создатель гильдии (первый лидер)
    founder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='founded_guilds', verbose_name="Основатель")
    
    # Лидер гильдии (может меняться)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_guilds', verbose_name="Лидер")
    
    # Публичность
    is_public = models.BooleanField(default=True, verbose_name="Публичная гильдия")
    # Код приглашения для закрытых гильдий
    invitation_code = models.CharField(max_length=50, blank=True, verbose_name="Код приглашения")
    
    # Статистика
    members_count = models.PositiveIntegerField(default=1, verbose_name="Количество участников")
    level = models.PositiveIntegerField(default=1, verbose_name="Уровень гильдии")
    experience = models.PositiveIntegerField(default=0, verbose_name="Опыт гильдии")
    gold_donated = models.PositiveIntegerField(default=0, verbose_name="Пожертвовано золота")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Гильдия"
        verbose_name_plural = "Гильдии"
        ordering = ['-level', '-experience']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генерируем slug, если он пустой
        if not self.slug:
            self.slug = slugify(self.name) + '-' + uuid.uuid4().hex[:6]
        # Если лидер не назначен, назначаем основателя
        if not self.leader and self.founder:
            self.leader = self.founder
        super().save(*args, **kwargs)

    def add_member(self, hero: Hero):
        """Добавляет героя в гильдию."""
        membership, created = GuildMembership.objects.get_or_create(
            guild=self,
            hero=hero,
            defaults={'role': 'member'}
        )
        if created:
            self.members_count = self.guild_memberships.count() # Обновляем счетчик
            self.save()
        return membership

    def remove_member(self, hero: Hero):
        """Удаляет героя из гильдии."""
        GuildMembership.objects.filter(guild=self, hero=hero).delete()
        self.members_count = self.guild_memberships.count() # Обновляем счетчик
        self.save()

from django.utils.text import slugify # Импортируем здесь

class GuildMembership(models.Model):
    """
    Связь между героем и гильдией.
    """
    ROLE_CHOICES = [
        ('leader', 'Лидер'),
        ('officer', 'Офицер'),
        ('member', 'Участник'),
        ('applicant', 'Заявитель'), # Для систем заявок
    ]
    
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='guild_memberships')
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE, related_name='guild_membership') # Герой может быть только в одной гильдии
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member', verbose_name="Роль")
    
    # Вклад участника
    experience_contributed = models.PositiveIntegerField(default=0, verbose_name="Внесено опыта")
    gold_contributed = models.PositiveIntegerField(default=0, verbose_name="Внесено золота")
    
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('guild', 'hero') # Уникальность участника в гильдии
        verbose_name = "Членство в гильдии"
        verbose_name_plural = "Членства в гильдиях"

    def __str__(self):
        return f"{self.hero.name} в {self.guild.name} ({self.get_role_display()})"

    def contribute_experience(self, amount: int):
        """Увеличивает вклад опыта участника и гильдии."""
        self.experience_contributed += amount
        self.guild.experience += amount
        self.save()
        self.guild.save()
        # TODO: Проверка на уровень гильдии

    def contribute_gold(self, amount: int):
        """Увеличивает вклад золота участника и гильдии."""
        self.gold_contributed += amount
        self.guild.gold_donated += amount
        # TODO: Списать золото у героя
        self.save()
        self.guild.save()

class GuildInvitation(models.Model):
    """
    Приглашение в гильдию.
    """
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='invitations')
    # Кого приглашают
    invited_hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='guild_invitations')
    # Кто пригласил
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    
    message = models.TextField(blank=True, verbose_name="Сообщение")
    is_accepted = models.BooleanField(default=False, verbose_name="Принято")
    is_declined = models.BooleanField(default=False, verbose_name="Отклонено")
    
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата ответа")

    class Meta:
        unique_together = ('guild', 'invited_hero') # Нельзя повторно пригласить того же героя
        verbose_name = "Приглашение в гильдию"
        verbose_name_plural = "Приглашения в гильдию"

    def __str__(self):
        status = "Принято" if self.is_accepted else ("Отклонено" if self.is_declined else "Ожидает")
        return f"Приглашение {self.invited_hero.name} в {self.guild.name} ({status})"

    def accept(self):
        """Принимает приглашение."""
        if not self.is_accepted and not self.is_declined:
            self.is_accepted = True
            self.is_declined = False
            self.responded_at = timezone.now()
            self.save()
            
            # Добавляем героя в гильдию
            self.guild.add_member(self.invited_hero)
            
            # Отправляем уведомление пригласившему
            from accounts.services import send_notification
            send_notification(
                self.invited_by,
                title=f"{self.invited_hero.name} принял приглашение!",
                message=f"Герой {self.invited_hero.name} присоединился к гильдии {self.guild.name} по вашему приглашению.",
                notification_type='success'
            )

    def decline(self):
        """Отклоняет приглашение."""
        if not self.is_accepted and not self.is_declined:
            self.is_declined = True
            self.is_accepted = False
            self.responded_at = timezone.now()
            self.save()
            
            # Отправляем уведомление пригласившему
            from accounts.services import send_notification
            send_notification(
                self.invited_by,
                title=f"{self.invited_hero.name} отклонил приглашение",
                message=f"Герой {self.invited_hero.name} отклонил приглашение в гильдию {self.guild.name}.",
                notification_type='info'
            )
