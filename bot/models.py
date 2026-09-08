from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class TelegramUser(models.Model):
    LANGUAGE_CHOICES = [
        ('uz', "O'zbekcha"),
        ('ru', "Русский"),
    ]

    telegram_id = models.BigIntegerField(unique=True, verbose_name=_("Telegram ID"))
    django_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("CRM Foydalanuvchisi")
    )
    is_authenticated = models.BooleanField(default=False, verbose_name=_("Tizimga kirgan"))
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Username"))
    full_name = models.CharField(max_length=255, verbose_name=_("To'liq ismi"))
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='uz',
        verbose_name=_("Tanlangan til")
    )
    is_admin = models.BooleanField(default=True, verbose_name=_("Admin ruxsati"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Ro'yxatdan o'tgan sana"))

    class Meta:
        verbose_name = _("Telegram Foydalanuvchi")
        verbose_name_plural = _("Telegram Foydalanuvchilar")
        ordering = ['-created_at']

    def __str__(self):
        auth_status = "✅ Login" if self.is_authenticated else "❌ Chiqqan"
        return f"{self.full_name} ({self.telegram_id}) - [{auth_status}]"
