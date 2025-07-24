# events/admin.py
from django.contrib import admin
from .models import Quest, HeroQuest

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'quest_type', 'required_level', 'is_approved', 'creator')
    list_filter = ('quest_type', 'is_approved', 'required_level')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HeroQuest)
class HeroQuestAdmin(admin.ModelAdmin):
    list_display = ('hero', 'quest', 'status', 'progress', 'started_at', 'completed_at')
    list_filter = ('status', 'quest')
    search_fields = ('hero__name', 'quest__title')
    readonly_fields = ('created_at', 'updated_at')
