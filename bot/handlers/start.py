from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import get_main_keyboard, get_auth_keyboard, get_language_inline_keyboard
from bot.services import (
    get_or_create_telegram_user,
    set_user_language,
)

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = await get_or_create_telegram_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name or "Foydalanuvchi",
    )
    lang = user.language

    if not user.is_authenticated:
        auth_text = get_text("auth_required", lang)
        await message.answer(
            text=auth_text,
            reply_markup=get_auth_keyboard(lang),
            parse_mode="HTML"
        )
        return

    welcome_text = get_text("welcome", lang, name=user.full_name or "")
    await message.answer(
        text=welcome_text,
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("lang:"))
async def language_callback_handler(callback: CallbackQuery):
    lang_code = callback.data.split(":")[1]
    await set_user_language(callback.from_user.id, lang_code)
    
    await callback.answer()
    msg_text = get_text("lang_changed", lang_code)
    await callback.message.edit_text(msg_text, parse_mode="HTML")

    user = await get_or_create_telegram_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name or "",
        default_lang=lang_code,
    )
    
    keyboard = get_main_keyboard(lang_code) if user.is_authenticated else get_auth_keyboard(lang_code)
    await callback.message.answer(
        text=get_text("main_menu_title", lang_code),
        reply_markup=keyboard,
        parse_mode="HTML"
    )
