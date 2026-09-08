from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'full_name',
        'username',
        'django_user',
        'is_authenticated',
        'language',
        'is_admin',
        'is_active',
        'created_at'
    )
    list_filter = ('is_authenticated', 'language', 'is_admin', 'is_active', 'created_at')
    search_fields = ('telegram_id', 'full_name', 'username', 'django_user__username')
    ordering = ('-created_at',)
    list_per_page = 25
