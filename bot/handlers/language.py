from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import get_language_inline_keyboard
from bot.services import get_user_language

router = Router()


@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык"]))
async def change_language_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    text = get_text("choose_language", lang)
    await message.answer(
        text=text,
        reply_markup=get_language_inline_keyboard()
    )
