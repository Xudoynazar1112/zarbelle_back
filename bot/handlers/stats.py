from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import get_main_keyboard, get_auth_keyboard
from bot.services import get_user_language, is_user_authenticated, get_crm_dashboard_stats

router = Router()


@router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
async def stats_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    if not await is_user_authenticated(message.from_user.id):
        await message.answer(get_text("auth_required", lang), reply_markup=get_auth_keyboard(lang), parse_mode="HTML")
        return

    stats = await get_crm_dashboard_stats()

    text = get_text(
        "stats_title",
        lang,
        total_customers=stats["total_customers"],
        connected_customers=stats["connected_customers"],
        not_connected_customers=stats["not_connected_customers"],
        lead_customers=stats["lead_customers"],
        trash_customers=stats["trash_customers"],
    )
    await message.answer(
        text=text,
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
