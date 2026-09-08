"""
Zar belle Telegram Bot - Ikki tilli (UZ / RU) matnlar va xabarlar lug'ati.
"""

MESSAGES = {
    # ---------------- BOSH MENYU VA START ----------------
    "welcome": {
        "uz": "Assalomu alaykum, <b>{name}</b>!\n<b>Zar belle CRM</b> botiga xush kelibsiz.\n\nKerakli bo'limni tanlang:",
        "ru": "Здравствуйте, <b>{name}</b>!\nДобро пожаловать в бот <b>Zar belle CRM</b>.\n\nВыберите нужный раздел:"
    },
    "choose_language": {
        "uz": "Iltimos, muloqot tilini tanlang:\nПожалуйста, выберите язык:",
        "ru": "Пожалуйста, выберите язык:\nIltimos, muloqot tilini tanlang:"
    },
    "lang_changed": {
        "uz": "✅ Til <b>O'zbekcha</b>ga o'zgartirildi.",
        "ru": "✅ Язык успешно изменен на <b>Русский</b>."
    },
    "main_menu_title": {
        "uz": "📱 <b>Bosh menyu:</b>",
        "ru": "📱 <b>Главное меню:</b>"
    },

    # ---------------- AUTENTIFIKATSIYA (LOGIN / LOGOUT) ----------------
    "auth_required": {
        "uz": (
            "🔒 <b>Tizimga kirish talab etiladi!</b>\n\n"
            "Zar belle CRM botidan foydalanish uchun CRM admin panelidagi <b>Login va Parolingiz</b> orqali avtorizatsiyadan o'ting.\n\n"
            "Boshlash uchun pastdagi <b>🔑 Tizimga kirish</b> tugmasini bosing:"
        ),
        "ru": (
            "🔒 <b>Требуется авторизация!</b>\n\n"
            "Для использования бота Zar belle CRM выполните вход с помощью вашего <b>Логина и Пароля</b> от CRM.\n\n"
            "Нажмите кнопку <b>🔑 Войти в систему</b> ниже:"
        )
    },
    "enter_username": {
        "uz": "👤 CRM tizimidagi <b>Login (Username)</b>ingizni kiriting:",
        "ru": "👤 Введите ваш <b>Логин (Username)</b> от CRM:"
    },
    "enter_password": {
        "uz": "🔑 <b>Parol</b>ingizni kiriting:",
        "ru": "🔑 Введите ваш <b>Пароль</b>:"
    },
    "login_success": {
        "uz": "🎉 <b>Xush kelibsiz, {user_name}!</b>\nSiz Zar belle CRM tizimiga muvaffaqiyatli kirdingiz.",
        "ru": "🎉 <b>Добро пожаловать, {user_name}!</b>\nВы успешно авторизовались в Zar belle CRM."
    },
    "login_failed": {
        "uz": "❌ <b>Login yoki parol noto'g'ri!</b>\nIltimos, qaytadan tekshirib urinib ko'ring.",
        "ru": "❌ <b>Неверный логин или пароль!</b>\nПожалуйста, проверьте данные и попробуйте снова."
    },
    "logged_out": {
        "uz": "🚪 Siz tizimdan muvaffaqiyatli chiqdingiz.",
        "ru": "🚪 Вы успешно вышли из системы."
    },
    "btn_login": {
        "uz": "🔑 Tizimga kirish",
        "ru": "🔑 Войти в систему"
    },
    "btn_logout": {
        "uz": "🚪 Chiqish",
        "ru": "🚪 Выйти"
    },

    # ---------------- MENYU TUGMALARI ----------------
    "btn_customers": {
        "uz": "👥 Mijozlar ro'yxati",
        "ru": "👥 Список клиентов"
    },
    "btn_add_customer": {
        "uz": "➕ Yangi mijoz qo'shish",
        "ru": "➕ Добавить клиента"
    },
    "btn_search": {
        "uz": "🔍 Qidiruv",
        "ru": "🔍 Поиск"
    },
    "btn_trash": {
        "uz": "🗑️ Korzinka",
        "ru": "🗑️ Корзина"
    },
    "btn_stats": {
        "uz": "📊 Statistika",
        "ru": "📊 Статистика"
    },
    "btn_change_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык"
    },
    "btn_cancel": {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена"
    },
    "btn_skip": {
        "uz": "⏭️ O'tkazib yuborish",
        "ru": "⏭️ Пропустить"
    },
    "btn_back": {
        "uz": "⬅️ Orqaga",
        "ru": "⬅️ Назад"
    },
    "btn_yes": {
        "uz": "✅ Ha",
        "ru": "✅ Да"
    },
    "btn_no": {
        "uz": "❌ Yo'q",
        "ru": "❌ Нет"
    },

    # ---------------- MIJOZLAR (CUSTOMERS) ----------------
    "customers_list_title": {
        "uz": "👥 <b>Mijozlar ro'yxati (Jami: {total}):</b>\nBatafsil ko'rish uchun mijozni tanlang:",
        "ru": "👥 <b>Список клиентов (Всего: {total}):</b>\nВыберите клиента для просмотра:"
    },
    "no_customers": {
        "uz": "📭 Hozircha mijozlar mavjud emas.",
        "ru": "📭 На данный момент клиентов нет."
    },
    "customer_card": {
        "uz": (
            "👤 <b>Mijoz kartasi:</b>\n\n"
            "🆔 ID: <code>#{id}</code>\n"
            "👤 Ism: <b>{name}</b>\n"
            "📞 Telefon: <b>{phone}</b>\n"
            "🔄 Bog'lanildi: {connected_icon} <b>{connected_text}</b>\n"
            "⭐️ Status: {lead_icon} <b>{lead_text}</b>\n"
            "📝 Izoh: <i>{comment}</i>\n"
            "📅 Yaratilgan: <code>{created_at}</code>"
        ),
        "ru": (
            "👤 <b>Карточка клиента:</b>\n\n"
            "🆔 ID: <code>#{id}</code>\n"
            "👤 Имя: <b>{name}</b>\n"
            "📞 Телефон: <b>{phone}</b>\n"
            "🔄 Связались: {connected_icon} <b>{connected_text}</b>\n"
            "⭐️ Статус: {lead_icon} <b>{lead_text}</b>\n"
            "📝 Комментарий: <i>{comment}</i>\n"
            "📅 Создан: <code>{created_at}</code>"
        )
    },
    "no_comment": {
        "uz": "Izoh yo'q",
        "ru": "Нет комментария"
    },
    "connected_yes": {"uz": "Bog'lanildi", "ru": "Связались"},
    "connected_no": {"uz": "Bog'lanilmadi", "ru": "Не связались"},
    "lead_yes": {"uz": "Potensial mijoz (Lead)", "ru": "Потенциальный клиент (Лид)"},
    "lead_no": {"uz": "Oddiy mijoz", "ru": "Обычный клиент"},

    "btn_toggle_connected": {
        "uz": "🔄 Bog'lanish holati: {status}",
        "ru": "🔄 Статус связи: {status}"
    },
    "btn_toggle_lead": {
        "uz": "⭐️ Lead holati: {status}",
        "ru": "⭐️ Статус Лида: {status}"
    },
    "btn_edit_comment": {
        "uz": "📝 Izohni tahrirlash",
        "ru": "📝 Изменить комментарий"
    },
    "btn_delete_customer": {
        "uz": "🗑️ O'chirish (Korzinkaga)",
        "ru": "🗑️ Удалить (В корзину)"
    },
    "customer_deleted": {
        "uz": "✅ Mijoz korzinkaga muvaffaqiyatli ko'chirildi (1 oy saqlanadi).",
        "ru": "✅ Клиент успешно перемещен в корзину (хранится 1 месяц)."
    },
    "status_updated": {
        "uz": "✅ Status yangilandi!",
        "ru": "✅ Статус обновлен!"
    },
    "enter_new_comment": {
        "uz": "📝 Mijoz uchun <b>yangi izoh</b> matnini kiriting:",
        "ru": "📝 Введите <b>новый комментарий</b> для клиента:"
    },
    "comment_updated": {
        "uz": "✅ Izoh muvaffaqiyatli yangilandi!",
        "ru": "✅ Комментарий успешно обновлен!"
    },

    # ---------------- YANGI MIJOZ QO'SHISH (FSM) ----------------
    "enter_customer_name": {
        "uz": "👤 Yangi mijozning <b>to'liq ismini</b> kiriting:",
        "ru": "👤 Введите <b>полное имя</b> нового клиента:"
    },
    "enter_customer_phone": {
        "uz": "📞 Mijozning <b>telefon raqamini</b> kiriting (masalan: +998901234567):",
        "ru": "📞 Введите <b>номер телефона</b> клиента (например: +998901234567):"
    },
    "ask_is_connected": {
        "uz": "🔄 Ushbu mijoz bilan bog'lanildimi?",
        "ru": "🔄 С этим клиентом уже связались?"
    },
    "ask_is_lead": {
        "uz": "⭐️ Bu mijoz <b>Potensial (Lead)</b> mijozmi?",
        "ru": "⭐️ Этот клиент является <b>Потенциальным (Лид)</b>?"
    },
    "ask_comment": {
        "uz": "📝 Mijoz haqida <b>izoh</b> kiriting (bog'lanish natijasi, nega lead bo'lgan/bo'lmagani) yoki o'tkazib yuboring:",
        "ru": "📝 Введите <b>комментарий</b> к клиенту (результат связи, причина статуса) или пропустите:"
    },
    "customer_added_success": {
        "uz": "🎉 <b>Mijoz muvaffaqiyatli qo'shildi!</b>\n\n👤 Ism: <b>{name}</b>\n📞 Telefon: <b>{phone}</b>",
        "ru": "🎉 <b>Клиент успешно добавлен!</b>\n\n👤 Имя: <b>{name}</b>\n📞 Телефон: <b>{phone}</b>"
    },
    "action_cancelled": {
        "uz": "❌ Amal bekor qilindi.",
        "ru": "❌ Действие отменено."
    },

    # ---------------- QIDIRUV (SEARCH) ----------------
    "enter_search_query": {
        "uz": "🔍 Qidirmoqchi bo'lgan mijozning <b>ismi, telefoni yoki izohini</b> kiriting:",
        "ru": "🔍 Введите <b>имя, телефон или комментарий</b> клиента для поиска:"
    },
    "search_results_title": {
        "uz": "🔍 <b>Qidiruv natijalari ('{query}', topildi: {total}):</b>",
        "ru": "🔍 <b>Результаты поиска ('{query}', найдено: {total}):</b>"
    },
    "search_not_found": {
        "uz": "🔍 '<b>{query}</b>' bo'yicha hech qanday mijoz topilmadi.",
        "ru": "🔍 По запросу '<b>{query}</b>' ничего не найдено."
    },

    # ---------------- KORZINKA (TRASH) ----------------
    "trash_list_title": {
        "uz": "🗑️ <b>Korzinka - O'chirilgan mijozlar (Jami: {total}):</b>\n<i>Bu yerda mijozlar 1 oy saqlanadi va qayta tiklanishi mumkin.</i>\n\nBatafsil ko'rish uchun tanlang:",
        "ru": "🗑️ <b>Корзина - Удаленные клиенты (Всего: {total}):</b>\n<i>Здесь клиенты хранятся 1 месяц и могут быть восстановлены.</i>\n\nВыберите для просмотра:"
    },
    "no_trash": {
        "uz": "🗑️ Korzinka bo'sh.",
        "ru": "🗑️ Корзина пуста."
    },
    "trash_card": {
        "uz": (
            "🗑️ <b>Korzinkadagi mijoz kartasi:</b>\n\n"
            "👤 Ism: <b>{name}</b>\n"
            "📞 Telefon: <b>{phone}</b>\n"
            "📝 Izoh: <i>{comment}</i>\n"
            "🗑️ O'chirilgan sana: <code>{deleted_at}</code>\n"
            "⏳ Saqlanish muddati tugashi: <code>{expires_at}</code>\n"
            "⚠️ Qolgan vaqt: <b>{days_left} kun</b>"
        ),
        "ru": (
            "🗑️ <b>Карточка удаленного клиента:</b>\n\n"
            "👤 Имя: <b>{name}</b>\n"
            "📞 Телефон: <b>{phone}</b>\n"
            "📝 Комментарий: <i>{comment}</i>\n"
            "🗑️ Дата удаления: <code>{deleted_at}</code>\n"
            "⏳ Срок хранения до: <code>{expires_at}</code>\n"
            "⚠️ Осталось: <b>{days_left} дн.</b>"
        )
    },
    "btn_restore_customer": {
        "uz": "♻️ Qayta tiklash (Restore)",
        "ru": "♻️ Восстановить"
    },
    "btn_hard_delete_customer": {
        "uz": "❌ Butunlay o'chirish",
        "ru": "❌ Удалить навсегда"
    },
    "customer_restored": {
        "uz": "🎉 <b>{name}</b> korzinkadan faol mijozlar ro'yxatiga qayta tiklandi!",
        "ru": "🎉 <b>{name}</b> успешно восстановлен из корзины в активные клиенты!"
    },
    "customer_hard_deleted": {
        "uz": "🗑️ Mijoz butunlay o'chirildi.",
        "ru": "🗑️ Клиент полностью удален."
    },

    # ---------------- STATISTIKA (STATS) ----------------
    "stats_title": {
        "uz": (
            "📊 <b>Zar belle CRM — Umumiy statistika:</b>\n\n"
            "👥 Jami faol mijozlar: <b>{total_customers} ta</b>\n"
            "📞 Bog'lanilgan: <b>{connected_customers} ta</b>\n"
            "⏳ Bog'lanilmagan: <b>{not_connected_customers} ta</b>\n"
            "⭐️ Potensial mijozlar (Lead): <b>{lead_customers} ta</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🗑️ Korzinkadagi mijozlar: <b>{trash_customers} ta</b>"
        ),
        "ru": (
            "📊 <b>Zar belle CRM — Общая статистика:</b>\n\n"
            "👥 Всего активных клиентов: <b>{total_customers}</b>\n"
            "📞 Связались: <b>{connected_customers}</b>\n"
            "⏳ Не связались: <b>{not_connected_customers}</b>\n"
            "⭐️ Потенциальные клиенты (Лиды): <b>{lead_customers}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🗑️ Клиентов в корзине: <b>{trash_customers}</b>"
        )
    },
}


def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    """Xabar kalitiga mos matnni tanlangan tilda qaytaradi."""
    lang = lang if lang in ["uz", "ru"] else "uz"
    item = MESSAGES.get(key)
    if not item:
        return key
    text = item.get(lang, item.get("uz", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
