# game_engine/tasks.py
"""
Celery задачи для периодического запуска игровых процессов.
"""
from celery import shared_task
from django.core.cache import cache
from django.conf import settings
from .engine import engine
from heroes.models import Hero
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_all_heroes():
    """
    Асинхронная задача: обрабатывает ходы всех героев.
    """
    logger.info("Начало обработки всех героев...")
    processed_count = 0
    logs = []
    for hero in Hero.objects.all():
        log_entry = engine.process_hero_turn(hero)
        logs.append(f"{hero.name}: {log_entry}")
        # Здесь можно сохранить лог в БД или кэш для отображения игроку
        cache.set(f"hero_log_{hero.id}", log_entry, timeout=3600) # Кэшируем на 1 час
        processed_count += 1
        
    logger.info(f"Обработано {processed_count} героев.")
    return f"Обработано {processed_count} героев."

@shared_task
def run_global_events():
    """
    Асинхронная задача: запускает глобальные события.
    """
    event_log = engine.run_global_events()
    # Можно кэшировать или отправлять уведомления
    cache.set("global_event_log", event_log, timeout=7200) # Кэшируем на 2 часа
    logger.info(f"Глобальное событие: {event_log}")
    return event_log

# Периодическая задача для обработки героев (например, каждые 10 минут)
from celery.schedules import crontab

# В settings.py или отдельном файле celery.py нужно настроить beat_schedule
# Например:
# CELERY_BEAT_SCHEDULE = {
#     'process-heroes-every-10-mins': {
#         'task': 'game_engine.tasks.process_all_heroes',
#         'schedule': 600.0, # 600 секунд = 10 минут
#     },
#     'run-global-events-hourly': {
#         'task': 'game_engine.tasks.run_global_events',
#         'schedule': crontab(minute=0), # Каждый час
#     },
# }
