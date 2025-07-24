# settings.py (фрагмент)
import os
from pathlib import Path

# ... стандартные настройки Django ...

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = ...

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'divine_heroes_db'),
        'USER': os.environ.get('DB_USER', 'divine_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Cache (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery Configuration (повторение для полноты картины)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')

# Celery Beat Schedule
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Обрабатываем всех героев каждые 10 минут
    'process-all-heroes': {
        'task': 'game_engine.tasks.process_all_heroes',
        'schedule': 600.0, # 600 секунд = 10 минут
    },
    # Запускаем глобальные события каждый час
    'run-global-events': {
        'task': 'game_engine.tasks.run_global_events',
        'schedule': crontab(minute=0), # Каждый час в 0 минут
    },
    # Можно добавить ежедневные задачи, например, воскрешение героев
    # 'resurrect-heroes-daily': {
    #     'task': 'game_engine.tasks.resurrect_heroes', # Нужно реализовать
    #     'schedule': crontab(hour=3, minute=0), # Ежедневно в 3:    # },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', # Наше приложение для аккаунтов
    'heroes',   # Наше приложение для героев
    'events',   # Наше приложение для событий
    # 'game_engine', # Модуль движка (не обязательно как приложение)
]

# ...
# LOGIN_REDIRECT_URL и LOGOUT_REDIRECT_URL
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ... остальные настройки ...
