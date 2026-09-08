from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_default_expiration():
    return timezone.now() + timedelta(days=30)


class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Mijoz ismi"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqami"))
    is_connected = models.BooleanField(default=False, verbose_name=_("Bog'lanildi"))
    is_lead = models.BooleanField(default=False, verbose_name=_("Potensial mijoz (Lead)"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Izoh"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))

    class Meta:
        verbose_name = _("Mijoz")
        verbose_name_plural = _("Mijozlar")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"


class CustomerTrash(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Mijoz ismi"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqami"))
    is_connected = models.BooleanField(default=False, verbose_name=_("Bog'lanildi"))
    is_lead = models.BooleanField(default=False, verbose_name=_("Potensial mijoz (Lead)"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Izoh"))
    original_created_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Dastlab yaratilgan sana"))
    deleted_at = models.DateTimeField(default=timezone.now, verbose_name=_("O'chirilgan sana"))
    expires_at = models.DateTimeField(default=get_default_expiration, verbose_name=_("Saqlanish muddati tugashi"))

    class Meta:
        verbose_name = _("Korzinkadagi mijoz")
        verbose_name_plural = _("Korzinka (O'chirilganlar)")
        ordering = ["-deleted_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def days_left(self) -> int:
        delta = self.expires_at - timezone.now()
        return max(0, delta.days)

    def restore(self) -> Customer:
        """Korzinkadagi mijozni qayta tiklash"""
        customer = Customer.objects.create(
            name=self.name,
            phone=self.phone,
            is_connected=self.is_connected,
            is_lead=self.is_lead,
            comment=self.comment,
        )
        self.delete()
        return customer
