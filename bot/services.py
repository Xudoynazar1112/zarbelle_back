from asgiref.sync import sync_to_async
from django.db.models import Q
from django.contrib.auth import authenticate
from django.utils import timezone
from crm.models import Customer, CustomerTrash
from .models import TelegramUser


@sync_to_async
def get_or_create_telegram_user(telegram_id: int, username: str, full_name: str, default_lang: str = "uz"):
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": username,
            "full_name": full_name,
            "language": default_lang,
            "is_authenticated": False,
        }
    )
    if not created:
        updated = False
        if user.full_name != full_name:
            user.full_name = full_name
            updated = True
        if user.username != username:
            user.username = username
            updated = True
        if updated:
            user.save()
    return user


@sync_to_async
def authenticate_and_login_user(telegram_id: int, username_input: str, password_input: str):
    """Django User login va paroli orqali tekshirish va TelegramUser ga bog'lash"""
    django_user = authenticate(username=username_input, password=password_input)
    if django_user is not None and django_user.is_active:
        telegram_user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
        if telegram_user:
            telegram_user.django_user = django_user
            telegram_user.is_authenticated = True
            telegram_user.is_admin = django_user.is_staff or django_user.is_superuser
            telegram_user.save()
            return django_user
    return None


@sync_to_async
def logout_telegram_user(telegram_id: int) -> bool:
    telegram_user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if telegram_user:
        telegram_user.is_authenticated = False
        telegram_user.save()
        return True
    return False


@sync_to_async
def is_user_authenticated(telegram_id: int) -> bool:
    telegram_user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    return telegram_user.is_authenticated if telegram_user else False


@sync_to_async
def get_user_language(telegram_id: int) -> str:
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    return user.language if user else "uz"


@sync_to_async
def set_user_language(telegram_id: int, language: str) -> bool:
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if user:
        user.language = language
        user.save()
        return True
    return False


@sync_to_async
def get_customers_list(page: int = 1, page_size: int = 5):
    total = Customer.objects.count()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = start + page_size
    customers = list(Customer.objects.all()[start:end])
    return customers, total, page, total_pages


@sync_to_async
def get_customer_by_id(customer_id: int):
    return Customer.objects.filter(id=customer_id).first()


@sync_to_async
def create_customer(name: str, phone: str, is_connected: bool = False, is_lead: bool = False, comment: str = None):
    return Customer.objects.create(
        name=name,
        phone=phone,
        is_connected=is_connected,
        is_lead=is_lead,
        comment=comment,
    )


@sync_to_async
def update_customer_comment(customer_id: int, comment: str):
    customer = Customer.objects.filter(id=customer_id).first()
    if customer:
        customer.comment = comment
        customer.save()
        return customer
    return None


@sync_to_async
def toggle_customer_field(customer_id: int, field: str):
    customer = Customer.objects.filter(id=customer_id).first()
    if customer and hasattr(customer, field):
        current_val = getattr(customer, field)
        setattr(customer, field, not current_val)
        customer.save()
        return customer
    return None


@sync_to_async
def delete_customer_to_trash(customer_id: int):
    customer = Customer.objects.filter(id=customer_id).first()
    if customer:
        customer.delete()  # Signal avtomatik CustomerTrash yaratadi
        return True
    return False


@sync_to_async
def get_trash_list(page: int = 1, page_size: int = 5):
    total = CustomerTrash.objects.count()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = start + page_size
    trash_items = list(CustomerTrash.objects.all()[start:end])
    return trash_items, total, page, total_pages


@sync_to_async
def get_trash_by_id(trash_id: int):
    return CustomerTrash.objects.filter(id=trash_id).first()


@sync_to_async
def restore_trash_customer(trash_id: int):
    trash_item = CustomerTrash.objects.filter(id=trash_id).first()
    if trash_item:
        restored = trash_item.restore()
        return restored
    return None


@sync_to_async
def hard_delete_trash_customer(trash_id: int):
    trash_item = CustomerTrash.objects.filter(id=trash_id).first()
    if trash_item:
        trash_item.delete()
        return True
    return False


@sync_to_async
def search_customers_db(query: str, page: int = 1, page_size: int = 5):
    qs = Customer.objects.filter(
        Q(name__icontains=query) | Q(phone__icontains=query) | Q(comment__icontains=query)
    )
    total = qs.count()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = start + page_size
    return list(qs[start:end]), total, page, total_pages


@sync_to_async
def get_crm_dashboard_stats():
    total_customers = Customer.objects.count()
    connected_customers = Customer.objects.filter(is_connected=True).count()
    not_connected_customers = Customer.objects.filter(is_connected=False).count()
    lead_customers = Customer.objects.filter(is_lead=True).count()
    trash_customers = CustomerTrash.objects.count()
    return {
        "total_customers": total_customers,
        "connected_customers": connected_customers,
        "not_connected_customers": not_connected_customers,
        "lead_customers": lead_customers,
        "trash_customers": trash_customers,
    }
