from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from .messages import get_text


def get_auth_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Tizimga kirish tugmasi"""
    keyboard = [
        [KeyboardButton(text=get_text("btn_login", lang))],
        [KeyboardButton(text=get_text("btn_change_lang", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Bosh menyu tugmalari"""
    keyboard = [
        [
            KeyboardButton(text=get_text("btn_customers", lang)),
            KeyboardButton(text=get_text("btn_add_customer", lang)),
        ],
        [
            KeyboardButton(text=get_text("btn_search", lang)),
            KeyboardButton(text=get_text("btn_trash", lang)),
        ],
        [
            KeyboardButton(text=get_text("btn_stats", lang)),
            KeyboardButton(text=get_text("btn_change_lang", lang)),
        ],
        [
            KeyboardButton(text=get_text("btn_logout", lang)),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_cancel_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi"""
    keyboard = [
        [KeyboardButton(text=get_text("btn_cancel", lang))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_skip_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """O'tkazib yuborish va Bekor qilish tugmasi"""
    keyboard = [
        [KeyboardButton(text=get_text("btn_skip", lang))],
        [KeyboardButton(text=get_text("btn_cancel", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_yes_no_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Ha / Yo'q va Bekor qilish tugmalari"""
    keyboard = [
        [
            KeyboardButton(text=get_text("btn_yes", lang)),
            KeyboardButton(text=get_text("btn_no", lang)),
        ],
        [KeyboardButton(text=get_text("btn_cancel", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_language_inline_keyboard() -> InlineKeyboardMarkup:
    """Tilni tanlash uchun inline klaviatura"""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_customers_list_keyboard(customers, page: int, total_pages: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Mijozlar ro'yxati va ixcham sahifalash (pagination) tugmalari"""
    inline_keyboard = []

    for c in customers:
        connected_mark = "✅" if c.is_connected else "⏳"
        lead_mark = "⭐️" if c.is_lead else ""
        btn_text = f"{connected_mark}{lead_mark} {c.name} ({c.phone})"
        inline_keyboard.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"view_customer:{c.id}:{page}")
        ])

    # Sahifalash (pagination) qatori
    if total_pages > 1:
        nav_row = []
        if page > 1:
            if page > 2:
                nav_row.append(InlineKeyboardButton(text="⏮️ 1", callback_data="customers_page:1"))
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"customers_page:{page - 1}"))
        
        nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data=f"page_info:{page}:{total_pages}"))

        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"customers_page:{page + 1}"))
            if page < total_pages - 1:
                nav_row.append(InlineKeyboardButton(text=f"{total_pages} ⏭️", callback_data=f"customers_page:{total_pages}"))

        inline_keyboard.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_customer_card_keyboard(customer_id: int, is_connected: bool, is_lead: bool, lang: str = "uz", page: int = 1) -> InlineKeyboardMarkup:
    """Mijoz kartasidagi boshqaruv tugmalari"""
    connected_status = "✅ " + get_text("btn_yes", lang) if is_connected else "❌ " + get_text("btn_no", lang)
    lead_status = "⭐️ " + get_text("lead_yes", lang) if is_lead else "⚪ " + get_text("lead_no", lang)

    buttons = [
        [
            InlineKeyboardButton(
                text=get_text("btn_toggle_connected", lang, status=connected_status),
                callback_data=f"toggle_connected:{customer_id}:{page}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_toggle_lead", lang, status=lead_status),
                callback_data=f"toggle_lead:{customer_id}:{page}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_edit_comment", lang),
                callback_data=f"edit_comment:{customer_id}:{page}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_delete_customer", lang),
                callback_data=f"delete_customer:{customer_id}:{page}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_back", lang),
                callback_data=f"customers_page:{page}"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_trash_list_keyboard(trash_items, page: int, total_pages: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Korzinkadagi mijozlar ro'yxati va sahifalash"""
    inline_keyboard = []

    for t in trash_items:
        btn_text = f"🗑️ {t.name} (⏳ {t.days_left}d)"
        inline_keyboard.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"view_trash:{t.id}:{page}")
        ])

    if total_pages > 1:
        nav_row = []
        if page > 1:
            if page > 2:
                nav_row.append(InlineKeyboardButton(text="⏮️ 1", callback_data="trash_page:1"))
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"trash_page:{page - 1}"))
        
        nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data=f"page_info:{page}:{total_pages}"))

        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"trash_page:{page + 1}"))
            if page < total_pages - 1:
                nav_row.append(InlineKeyboardButton(text=f"{total_pages} ⏭️", callback_data=f"trash_page:{total_pages}"))

        inline_keyboard.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_trash_card_keyboard(trash_id: int, lang: str = "uz", page: int = 1) -> InlineKeyboardMarkup:
    """Korzinkadagi mijoz kartasi tugmalari"""
    buttons = [
        [
            InlineKeyboardButton(
                text=get_text("btn_restore_customer", lang),
                callback_data=f"restore_trash:{trash_id}:{page}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_hard_delete_customer", lang),
                callback_data=f"hard_delete_trash:{trash_id}:{page}"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_back", lang),
                callback_data=f"trash_page:{page}"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_search_results_keyboard(results, query: str, page: int, total_pages: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Qidiruv natijalari uchun sahifalash tugmalari"""
    inline_keyboard = []

    for c in results:
        connected_mark = "✅" if c.is_connected else "⏳"
        lead_mark = "⭐️" if c.is_lead else ""
        btn_text = f"{connected_mark}{lead_mark} {c.name} ({c.phone})"
        inline_keyboard.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"view_customer:{c.id}:1")
        ])

    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"search_page:{query}:{page - 1}"))
        
        nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data=f"page_info:{page}:{total_pages}"))

        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"search_page:{query}:{page + 1}"))

        inline_keyboard.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
