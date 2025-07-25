# events/views.py (новый файл)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Item, Inventory, Equipment, Quest, HeroQuest
from .forms import UserQuestForm
from heroes.models import Hero

@login_required
def inventory_view(request):
    """Отображает инвентарь героя."""
    hero = get_object_or_404(Hero, owner=request.user)
    inventory_items = hero.inventory_items.all()
    equipment = getattr(hero, 'equipment', None)
    
    context = {
        'hero': hero,
        'inventory_items': inventory_items,
        'equipment': equipment,
    }
    return render(request, 'events/inventory.html', context)

@login_required
def equip_item(request, item_id):
    """Экипирует предмет."""
    hero = get_object_or_404(Hero, owner=request.user)
    item = get_object_or_404(Item, id=item_id)
    inventory_item = get_object_or_404(Inventory, hero=hero, item=item)
    
    # Проверка, есть ли предмет в инвентаре
    if inventory_item.quantity <= 0:
        messages.error(request, "У вас нет этого предмета.")
        return redirect('events:inventory')
    
    equipment, created = Equipment.objects.get_or_create(hero=hero)
    result_message = equipment.equip_item(item)
    messages.info(request, result_message)
    
    return redirect('events:inventory')

@login_required
def unequip_item(request, item_type):
    """Снимает предмет из слота."""
    hero = get_object_or_404(Hero, owner=request.user)
    equipment = get_object_or_404(Equipment, hero=hero)
    
    result_message = equipment.unequip_item(item_type)
    messages.info(request, result_message)
    
    return redirect('events:inventory')

@login_required
def use_item(request, item_id):
    """Использует предмет из инвентаря."""
    hero = get_object_or_404(Hero, owner=request.user)
    inventory_item = get_object_or_404(Inventory, hero=hero, item_id=item_id)
    
    # Вызываем метод использования из модели Inventory
    result_message = inventory_item.use_item()
    messages.info(request, result_message)
    
    return redirect('events:inventory')

@login_required
def create_user_quest(request):
    """Позволяет пользователю создать свой квест."""
    if request.method == 'POST':
        form = UserQuestForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.creator = request.user
            quest.quest_type = 'user_generated'
            quest.is_approved = False # Требует модерации
            quest.save()
            messages.success(request, 'Ваш квест отправлен на модерацию. Спасибо за вклад!')
            return redirect('events:user_quests_list') # Перенаправляем на список своих квестов
    else:
        form = UserQuestForm()
    return render(request, 'events/create_user_quest.html', {'form': form})

@login_required
def user_quests_list(request):
    """Отображает список квестов, созданных текущим пользователем."""
    user_quests = Quest.objects.filter(creator=request.user).order_by('-created_at')
    
    # Пагинация (опционально, но полезно)
    paginator = Paginator(user_quests, 10) # 10 квестов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/user_quests_list.html', {'page_obj': page_obj})

def public_quests_list(request):
    """Отображает список одобренных квестов (системных и пользовательских)."""
    # Показываем только одобренные квесты, сортируем по дате создания
    approved_quests = Quest.objects.filter(is_approved=True).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(approved_quests, 15) # 15 квестов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/public_quests_list.html', {'page_obj': page_obj})
