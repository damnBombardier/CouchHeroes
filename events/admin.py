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

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'rarity', 'power', 'defense', 'healing_amount', 'sell_price')
    list_filter = ('item_type', 'rarity')
    search_fields = ('name', 'description')

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('hero', 'item', 'quantity')
    list_filter = ('item__item_type', 'item__rarity')
    search_fields = ('hero__name', 'item__name')

# Или используем Inline для отображения в админке героя
# class InventoryInline(admin.TabularInline):
#     model = Inventory
#     extra = 0

admin.site.register(Inventory, InventoryAdmin)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('hero', 'weapon', 'armor')
    search_fields = ('hero__name',)
