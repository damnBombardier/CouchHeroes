# heroes/urls.py
from django.urls import path
from . import views

app_name = 'heroes'
urlpatterns = [
    path('detail/', views.hero_detail, name='detail'),
    path('action/<str:action_type>/', views.hero_action, name='action'),
    # path('action/lightning/', views.hero_lightning, name='lightning'),
    # path('action/speech/', views.hero_speech, name='speech'),
]
