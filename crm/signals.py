from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Customer, CustomerTrash


@receiver(pre_delete, sender=Customer)
def move_customer_to_trash(sender, instance, **kwargs):
    """
    Customer o'chirilganda (Admin panel, API yoki ORM orqali),
    uni avtomatik Korzinkaga (CustomerTrash) saqlash.
    """
    if not getattr(instance, '_skip_trash', False):
        CustomerTrash.objects.create(
            name=instance.name,
            phone=instance.phone,
            is_connected=instance.is_connected,
            is_lead=instance.is_lead,
            comment=instance.comment,
            original_created_at=instance.created_at,
        )
