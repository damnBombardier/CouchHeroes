# accounts/services.py (новый файл)
from django.contrib.auth.models import User
from .models import Notification
from heroes.models import Hero # Для ссылок на героя
# from django.urls import reverse # Для генерации ссылок
# from django.conf import settings # Для настроек (например, email)

def send_notification(user: User, title: str, message: str, notification_type='info', link=None):
    """
    Отправляет уведомление пользователю.
    """
    # TODO: Добавить отправку email или push-уведомлений в будущем
    notification = Notification.objects.create(
        recipient=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link
    )
    return notification

def send_hero_notification(hero: Hero, title: str, message: str, notification_type='info'):
    """
    Отправляет уведомление владельцу героя.
    Автоматически создает ссылку на страницу героя.
    """
    # from django.urls import reverse # Импортируем здесь, чтобы избежать циклических импортов
    # link = reverse('heroes:detail') # Простая ссылка на героя
    # Для более точной ссылки на конкретого героя потребуются дополнительные настройки URL
    link = '/heroes/' # Пока так
    return send_notification(
        user=hero.owner,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link
    )

# ... (можно добавить другие специфичные функции, например, send_quest_completed_notification)
