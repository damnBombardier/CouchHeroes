# events/urls.py (новый файл)
from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('inventory/', views.inventory_view, name='inventory'),
    path('equip/<int:item_id>/', views.equip_item, name='equip_item'),
    path('unequip/<str:item_type>/', views.unequip_item, name='unequip_item'),
    path('use/<int:item_id>/', views.use_item, name='use_item'), # Добавлено
]
