from django.test import TestCase
from django.contrib.auth.models import User
from crm.models import Customer, CustomerTrash
from bot.models import TelegramUser
from bot.messages import MESSAGES, get_text
from bot.keyboards import (
    get_main_keyboard,
    get_auth_keyboard,
    get_cancel_keyboard,
    get_skip_keyboard,
    get_yes_no_keyboard,
    get_customer_card_keyboard,
    get_trash_card_keyboard,
    get_customers_list_keyboard,
    get_trash_list_keyboard,
)
from bot.services import (
    get_or_create_telegram_user,
    authenticate_and_login_user,
    logout_telegram_user,
    is_user_authenticated,
    get_user_language,
    set_user_language,
    get_customers_list,
    get_customer_by_id,
    create_customer,
    update_customer_comment,
    toggle_customer_field,
    delete_customer_to_trash,
    get_trash_list,
    get_trash_by_id,
    restore_trash_customer,
    hard_delete_trash_customer,
    search_customers_db,
    get_crm_dashboard_stats,
)


class BotAppTestCase(TestCase):
    async def test_telegram_user_auth_and_language_services(self):
        # 1. Django User yaratamiz
        await User.objects.acreate(
            username="zar_manager",
            password="secretpassword123",
            is_staff=True,
        )
        # Parolni to'g'ri hash qilish uchun set_password
        user_obj = await User.objects.aget(username="zar_manager")
        user_obj.set_password("secretpassword123")
        await user_obj.asave()

        # 2. Telegram foydalanuvchi yaratish
        telegram_user = await get_or_create_telegram_user(
            telegram_id=987654321,
            username="manager_tg",
            full_name="Manager Name",
            default_lang="uz"
        )
        self.assertEqual(telegram_user.telegram_id, 987654321)
        self.assertFalse(await is_user_authenticated(987654321))

        # 3. Noto'g'ri parol bilan kirishga urinish
        fail_login = await authenticate_and_login_user(987654321, "zar_manager", "wrongpassword")
        self.assertIsNone(fail_login)
        self.assertFalse(await is_user_authenticated(987654321))

        # 4. To'g'ri login va parol bilan kirish
        success_login = await authenticate_and_login_user(987654321, "zar_manager", "secretpassword123")
        self.assertIsNotNone(success_login)
        self.assertTrue(await is_user_authenticated(987654321))

        # 5. Chiqish (Logout)
        logged_out = await logout_telegram_user(987654321)
        self.assertTrue(logged_out)
        self.assertFalse(await is_user_authenticated(987654321))

    async def test_bot_crm_services_with_comment_workflow(self):
        # 1. Mijoz yaratish (izoh bilan)
        customer = await create_customer(
            name="Temur Malik",
            phone="+998901112233",
            is_connected=False,
            is_lead=False,
            comment="Birinchi marta qo'ng'iroq qilindi."
        )
        self.assertEqual(customer.name, "Temur Malik")
        self.assertEqual(customer.comment, "Birinchi marta qo'ng'iroq qilindi.")

        # 2. Izohni yangilash
        updated_cust = await update_customer_comment(customer.id, "Qayta bog'lanildi, taklif yuborildi.")
        self.assertEqual(updated_cust.comment, "Qayta bog'lanildi, taklif yuborildi.")

        # 3. Statuslarni o'zgartirish (Toggle)
        updated = await toggle_customer_field(customer.id, "is_connected")
        self.assertTrue(updated.is_connected)

        updated_lead = await toggle_customer_field(customer.id, "is_lead")
        self.assertTrue(updated_lead.is_lead)

        # 4. Statistika tekshirish
        stats = await get_crm_dashboard_stats()
        self.assertEqual(stats["total_customers"], 1)
        self.assertEqual(stats["connected_customers"], 1)
        self.assertEqual(stats["lead_customers"], 1)
        self.assertEqual(stats["trash_customers"], 0)

        # 5. Izoh bo'yicha qidiruv
        search_res = await search_customers_db("taklif")
        self.assertEqual(len(search_res), 1)

        # 6. O'chirish (Korzinkaga o'tish)
        deleted = await delete_customer_to_trash(customer.id)
        self.assertTrue(deleted)

        trash_items, total, page, total_pages = await get_trash_list(page=1)
        self.assertEqual(total, 1)
        self.assertEqual(trash_items[0].name, "Temur Malik")
        self.assertEqual(trash_items[0].comment, "Qayta bog'lanildi, taklif yuborildi.")

        # 7. Qayta tiklash (Restore)
        restored = await restore_trash_customer(trash_items[0].id)
        self.assertIsNotNone(restored)
        self.assertEqual(restored.name, "Temur Malik")
        self.assertEqual(restored.comment, "Qayta bog'lanildi, taklif yuborildi.")

    def test_messages_dictionary_completeness(self):
        # Barcha xabarlar UZ va RU tillarida mavjudligini tekshirish
        for key, translations in MESSAGES.items():
            self.assertIn("uz", translations, f"Key '{key}' is missing 'uz' translation")
            self.assertIn("ru", translations, f"Key '{key}' is missing 'ru' translation")
            self.assertTrue(len(translations["uz"]) > 0)
            self.assertTrue(len(translations["ru"]) > 0)

        # get_text helper tekshirish
        uz_txt = get_text("btn_customers", "uz")
        ru_txt = get_text("btn_customers", "ru")
        self.assertEqual(uz_txt, "👥 Mijozlar ro'yxati")
        self.assertEqual(ru_txt, "👥 Список клиентов")

    def test_keyboards_generation(self):
        main_kb_uz = get_main_keyboard("uz")
        main_kb_ru = get_main_keyboard("ru")
        self.assertEqual(len(main_kb_uz.keyboard), 4)
        self.assertEqual(len(main_kb_ru.keyboard), 4)

        auth_kb = get_auth_keyboard("uz")
        self.assertEqual(auth_kb.keyboard[0][0].text, "🔑 Tizimga kirish")

        skip_kb = get_skip_keyboard("uz")
        self.assertEqual(skip_kb.keyboard[0][0].text, "⏭️ O'tkazib yuborish")
