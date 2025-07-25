# guilds/admin.py (новый файл)
from django.contrib import admin
from .models import Guild, GuildMembership, GuildInvitation

@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'members_count', 'level', 'is_public', 'created_at')
    list_filter = ('is_public', 'level', 'created_at')
    search_fields = ('name', 'description', 'motto')
    prepopulated_fields = {"slug": ("name",)} # Автозаполнение slug из name
    readonly_fields = ('created_at', 'updated_at')

@admin.register(GuildMembership)
class GuildMembershipAdmin(admin.ModelAdmin):
    list_display = ('hero', 'guild', 'role', 'joined_at')
    list_filter = ('role', 'guild', 'joined_at')
    search_fields = ('hero__name', 'guild__name')

@admin.register(GuildInvitation)
class GuildInvitationAdmin(admin.ModelAdmin):
    list_display = ('invited_hero', 'guild', 'invited_by', 'is_accepted', 'is_declined', 'created_at')
    list_filter = ('is_accepted', 'is_declined', 'guild', 'created_at')
    search_fields = ('invited_hero__name', 'guild__name', 'invited_by__username')
    readonly_fields = ('created_at', 'responded_at')
