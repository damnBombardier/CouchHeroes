# heroes/urls.py
from django.urls import path
from . import views

app_name = 'heroes'
urlpatterns = [
    path('', views.hero_detail, name='detail'), # Главная страница модуля
    path('detail/data/', views.hero_detail_data, name='detail_data'), # Для AJAX
    path('action/<str:action_type>/', views.hero_action, name='action'),
]
