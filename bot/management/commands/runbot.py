import asyncio
import logging
import os
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from bot.handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_bot():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN .env faylida topilmadi! Iltimos, .env fayliga BOT_TOKEN=... ni kiriting.")

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    main_router = register_all_handlers()
    dp.include_router(main_router)

    logger.info("Zar belle Telegram Bot muvaffaqiyatli ishga tushirildi!")
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = "Zar belle CRM Telegram botini ishga tushirish (Polling)"

    def handle(self, *args, **options):
        try:
            asyncio.run(start_bot())
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.WARNING("Bot to'xtatildi."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Xatolik: {e}"))
