# heroes/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Hero
from game_engine.engine import engine
from django.core.cache import cache

@login_required
def hero_detail(request):
    """
    Отображает страницу героя текущего пользователя.
    """
    hero = get_object_or_404(Hero, owner=request.user)
    # Получаем последний лог из кэша (или из БД)
    last_action = cache.get(f"hero_log_{hero.id}", "Герой готов к приключениям!")
    
    context = {
        'hero': hero,
        'last_action': last_action,
    }
    return render(request, 'heroes/detail.html', context)

@login_required
def hero_detail_data(request):
    """
    Возвращает данные героя в формате JSON для AJAX обновления.
    """
    hero = get_object_or_404(Hero, owner=request.user)
    last_action = cache.get(f"hero_log_{hero.id}", "Герой готов к приключениям!")
    
    data = {
        'name': hero.name,
        'level': hero.level,
        'health': hero.health,
        'max_health': hero.max_health,
        'gold': hero.gold,
        'experience': hero.experience,
        'state': hero.get_state_display(),
        'location': hero.location,
        'monsters_killed': hero.monsters_killed,
        'deaths': hero.deaths,
        'last_action': last_action,
    }
    return JsonResponse(data)

@login_required
def hero_action(request, action_type):
    """
    Обрабатывает действия игрока (молния, реплика).
    """
    hero = get_object_or_404(Hero, owner=request.user)
    result = ""
    
    if action_type == 'lightning':
        result = hero.apply_lightning_strike()
    elif action_type == 'speech':
        # В реальном приложении текст реплики должен передаваться в запросе
        message = request.GET.get('message', 'Будь храбр!')
        result = hero.apply_divine_speech(message)
    else:
        return JsonResponse({'error': 'Неизвестное действие'}, status=400)
        
    # Обновляем кэш с последним действием
    cache.set(f"hero_log_{hero.id}", result, timeout=3600)
    
    return JsonResponse({'message': result})
