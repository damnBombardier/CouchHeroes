# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import PlayerProfile, Notification # Добавлен импорт Notification
from heroes.models import Hero

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан! Вы можете войти.')
            # Автоматически создаем героя для нового пользователя
            # Логика создания героя
            hero_name = f"{username}'s Hero" # Простое имя, можно усложнить
            # Проверим, нет ли уже героя (на случай, если сигнал не сработал)
            if not hasattr(user, 'hero'):
                 Hero.objects.create(name=hero_name, owner=user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(PlayerProfile, user=user)
    # Получаем героя пользователя
    hero = get_object_or_404(Hero, owner=user)
    context = {
        'profile_user': user,
        'profile': profile,
        'hero': hero,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def notifications_list(request):
    """Отображает список уведомлений пользователя."""
    user_notifications = request.user.notifications.all()
    
    # Пагинация
    paginator = Paginator(user_notifications, 10) # 10 уведомлений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Помечаем непрочитанные уведомления как прочитанные при просмотре списка
    unread_notifications = user_notifications.filter(is_read=False)
    for notif in unread_notifications:
        notif.mark_as_read()
    
    return render(request, 'accounts/notifications_list.html', {'page_obj': page_obj})

@login_required
def mark_notification_read(request, notification_id):
    """Помечает конкретное уведомление как прочитанное."""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    # Перенаправляем обратно на список или по ссылке из уведомления
    next_url = request.GET.get('next', 'accounts:notifications_list')
    return redirect(next_url)
