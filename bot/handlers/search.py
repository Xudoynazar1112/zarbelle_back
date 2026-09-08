from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import get_main_keyboard, get_auth_keyboard, get_cancel_keyboard, get_search_results_keyboard
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

    results, total, page, total_pages = await search_customers_db(query, page=1)

    if not results:
        await message.answer(
            text=get_text("search_not_found", lang, query=query),
            reply_markup=get_main_keyboard(lang),
            parse_mode="HTML"
        )
        return

    text = get_text("search_results_title", lang, query=query, total=total)
    keyboard = get_search_results_keyboard(results, query, page, total_pages, lang)
    await message.answer(text=text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("search_page:"))
async def search_page_callback(callback: CallbackQuery):
    _, query, page = callback.data.split(":")
    page = int(page)
    lang = await get_user_language(callback.from_user.id)
    results, total, page, total_pages = await search_customers_db(query, page=page)

    if not results:
        await callback.answer(get_text("search_not_found", lang, query=query), show_alert=True)
        return

    text = get_text("search_results_title", lang, query=query, total=total)
    keyboard = get_search_results_keyboard(results, query, page, total_pages, lang)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
