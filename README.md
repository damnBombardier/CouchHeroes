# Divine Heroes (Диванные герои)

Текстовая многопользовательская ZPG (Zero Player Game), где игроки выступают в роли богов, косвенно влияющих на своих героев-почитателей.

## Особенности

*   **ZPG**: Герои действуют автономно.
*   **Текстовый интерфейс**: Насыщенные юмором и аллюзиями тексты.
*   **Вмешательство бога**: Молнии и реплики.
*   **Сообщество**: Возможность создания пользовательского контента (в будущем).

## Технологии

*   **Бэкенд**: Python, Django
*   **База данных**: PostgreSQL
*   **Кэш/Очередь задач**: Redis, Celery
*   **Фронтенд**: HTML, CSS, JavaScript (Vanilla)

## Установка и запуск (для разработки)

1.  Установите Python 3.8+
2.  Создайте виртуальное окружение: `python -m venv venv`
3.  Активируйте его: `source venv/bin/activate` (Linux/Mac) или `venv\Scripts\activate` (Windows)
4.  Установите зависимости: `pip install -r requirements.txt`
5.  Создайте файл `.env` с настройками БД и Redis (пример в `settings.py`).
6.  Примените миграции: `python manage.py migrate`
7.  Создайте суперпользователя: `python manage.py createsuperuser`
8.  Запустите сервер разработки: `python manage.py runserver`
9.  (В отдельном терминале) Запустите Celery worker: `celery -A divine_heroes worker -l info`
10. (В отдельном терминале) Запустите Celery beat для периодических задач: `celery -A divine_heroes beat -l info`
