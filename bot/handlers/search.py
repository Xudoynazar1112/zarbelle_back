from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import get_main_keyboard, get_auth_keyboard, get_cancel_keyboard
from bot.states import SearchCustomerState
from bot.services import get_user_language, is_user_authenticated, search_customers_db

router = Router()


@router.message(F.text.in_(["🔍 Qidiruv", "🔍 Поиск"]))
async def search_start_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    if not await is_user_authenticated(message.from_user.id):
        await message.answer(get_text("auth_required", lang), reply_markup=get_auth_keyboard(lang), parse_mode="HTML")
        return

    await state.set_state(SearchCustomerState.query)
    await message.answer(
        text=get_text("enter_search_query", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(SearchCustomerState.query)
async def search_query_handler(message: Message, state: FSMContext):
    query = message.text.strip()
    lang = await get_user_language(message.from_user.id)
    await state.clear()

    results = await search_customers_db(query)

    if not results:
        await message.answer(
            text=get_text("search_not_found", lang, query=query),
            reply_markup=get_main_keyboard(lang),
            parse_mode="HTML"
        )
        return

    text = get_text("search_results_title", lang, query=query, total=len(results))
    buttons = []
    for c in results:
        connected_mark = "✅" if c.is_connected else "⏳"
        lead_mark = "⭐️" if c.is_lead else ""
        btn_text = f"{connected_mark}{lead_mark} {c.name} ({c.phone})"
        buttons.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"view_customer:{c.id}:1")
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await message.answer(
        text=get_text("main_menu_title", lang),
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
