# divine_heroes/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('heroes/', include('heroes.urls')),
    path('events/', include('events.urls')), # Добавлено
    path('', include('heroes.urls')), # Главная страница - страница героя
]
