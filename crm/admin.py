from django.contrib import admin
from django import forms
from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Customer, CustomerTrash


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'is_connected', 'is_lead', 'comment', 'created_at')
    list_editable = ('is_connected', 'is_lead', 'comment')
    list_display_links = ('id', 'name')
    list_filter = ('is_connected', 'is_lead', 'created_at')
    search_fields = ('name', 'phone', 'comment')
    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'

    # Jadvaldagi izoh (comment) maydonini ixcham va chiroyli bitta qatorli input qilish
    formfield_overrides = {
        models.TextField: {
            'widget': forms.TextInput(attrs={
                'class': 'form-control form-control-sm compact-comment-input',
                'placeholder': _("Izoh..."),
            })
        },
    }

    actions = [
        'mark_as_connected',
        'mark_as_not_connected',
        'mark_as_lead',
        'mark_as_not_lead',
    ]

    @admin.action(description=_("Tanlanganlarni 'Bog'lanildi' qilish"))
    def mark_as_connected(self, request, queryset):
        count = queryset.update(is_connected=True)
        self.message_user(request, f"{count} ta mijoz 'Bog'lanildi' qilindi.")

    @admin.action(description=_("Tanlanganlarni 'Bog'lanilmadi' qilish"))
    def mark_as_not_connected(self, request, queryset):
        count = queryset.update(is_connected=False)
        self.message_user(request, f"{count} ta mijoz 'Bog'lanilmadi' qilindi.")

    @admin.action(description=_("Tanlanganlarni 'Lead' qilish"))
    def mark_as_lead(self, request, queryset):
        count = queryset.update(is_lead=True)
        self.message_user(request, f"{count} ta mijoz 'Lead' qilindi.")

    @admin.action(description=_("Tanlanganlarni 'Oddiy mijoz' qilish"))
    def mark_as_not_lead(self, request, queryset):
        count = queryset.update(is_lead=False)
        self.message_user(request, f"{count} ta mijoz 'Oddiy mijoz' qilindi.")


@admin.register(CustomerTrash)
class CustomerTrashAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'is_connected_badge',
        'is_lead_badge',
        'comment',
        'deleted_at',
        'expires_at',
        'days_left_badge'
    )
    list_filter = ('is_connected', 'is_lead', 'deleted_at')
    search_fields = ('name', 'phone', 'comment')
    ordering = ('-deleted_at',)
    list_per_page = 25
    date_hierarchy = 'deleted_at'
    actions = ['restore_selected_customers', 'clear_expired_trash']

    def has_add_permission(self, request):
        return False

    @admin.display(description=_("Bog'lanildi"))
    def is_connected_badge(self, obj):
        if obj.is_connected:
            return format_html('<span class="badge badge-success">{}</span>', _("Ha"))
        return format_html('<span class="badge badge-secondary">{}</span>', _("Yo'q"))

    @admin.display(description=_("Lead"))
    def is_lead_badge(self, obj):
        if obj.is_lead:
            return format_html('<span class="badge badge-primary">Lead</span>')
        return format_html('<span class="badge badge-light">{}</span>', _("Oddiy"))

    @admin.display(description=_("Qolgan saqlanish muddati"))
    def days_left_badge(self, obj):
        days = obj.days_left
        if obj.is_expired:
            return format_html('<span class="badge badge-danger">{}</span>', _("Muddati tugagan"))
        elif days <= 3:
            return format_html('<span class="badge badge-danger">{} {}</span>', days, _("kun qoldi"))
        elif days <= 7:
            return format_html('<span class="badge badge-warning">{} {}</span>', days, _("kun qoldi"))
        else:
            return format_html('<span class="badge badge-info">{} {}</span>', days, _("kun qoldi"))

    @admin.action(description=_("Tanlangan mijozlarni qayta tiklash (Restore)"))
    def restore_selected_customers(self, request, queryset):
        count = 0
        for item in queryset:
            item.restore()
            count += 1
        self.message_user(request, f"{count} ta mijoz korzinkadan faol mijozlar ro'yxatiga muvaffaqiyatli qaytarildi.")

    @admin.action(description=_("Muddati o'tgan mijozlarni tozalash (30 kundan oshganlar)"))
    def clear_expired_trash(self, request, queryset):
        expired = queryset.filter(expires_at__lte=timezone.now())
        count = expired.count()
        expired.delete()
        self.message_user(request, f"{count} ta muddati o'tgan yozuv butunlay o'chirildi.")
