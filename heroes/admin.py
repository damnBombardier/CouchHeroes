# heroes/admin.py
from django.contrib import admin
from .models import Hero

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'level', 'state', 'health', 'gold')
    list_filter = ('state', 'level')
    search_fields = ('name', 'owner__username')
    readonly_fields = ('created_at', 'updated_at', 'last_updated')
