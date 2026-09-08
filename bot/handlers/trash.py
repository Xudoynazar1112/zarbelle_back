from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import (
    get_main_keyboard,
    get_auth_keyboard,
    get_trash_list_keyboard,
    get_trash_card_keyboard,
)
from bot.services import (
    get_user_language,
    is_user_authenticated,
    get_trash_list,
    get_trash_by_id,
    restore_trash_customer,
    hard_delete_trash_customer,
)

router = Router()


@router.message(F.text.in_(["🗑️ Korzinka", "🗑️ Корзина"]))
async def trash_list_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    if not await is_user_authenticated(message.from_user.id):
        await message.answer(get_text("auth_required", lang), reply_markup=get_auth_keyboard(lang), parse_mode="HTML")
        return

    trash_items, total, page, total_pages = await get_trash_list(page=1)

    if not trash_items:
        await message.answer(
            text=get_text("no_trash", lang),
            reply_markup=get_main_keyboard(lang)
        )
        return

    text = get_text("trash_list_title", lang, total=total)
    keyboard = get_trash_list_keyboard(trash_items, page, total_pages, lang)
    await message.answer(text=text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("trash_page:"))
async def trash_page_callback(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    lang = await get_user_language(callback.from_user.id)
    trash_items, total, page, total_pages = await get_trash_list(page=page)

    if not trash_items:
        await callback.message.edit_text(get_text("no_trash", lang))
        await callback.answer()
        return

    text = get_text("trash_list_title", lang, total=total)
    keyboard = get_trash_list_keyboard(trash_items, page, total_pages, lang)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("view_trash:"))
async def view_trash_callback(callback: CallbackQuery):
    _, trash_id, page = callback.data.split(":")
    trash_id, page = int(trash_id), int(page)
    lang = await get_user_language(callback.from_user.id)
    trash_item = await get_trash_by_id(trash_id)

    if not trash_item:
        await callback.answer(get_text("no_trash", lang), show_alert=True)
        return

    comment_text = trash_item.comment if trash_item.comment else get_text("no_comment", lang)

    text = get_text(
        "trash_card",
        lang,
        name=trash_item.name,
        phone=trash_item.phone,
        comment=comment_text,
        deleted_at=trash_item.deleted_at.strftime("%d.%m.%Y %H:%M"),
        expires_at=trash_item.expires_at.strftime("%d.%m.%Y %H:%M"),
        days_left=trash_item.days_left
    )
    keyboard = get_trash_card_keyboard(trash_item.id, lang, page)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("restore_trash:"))
async def restore_trash_callback(callback: CallbackQuery):
    _, trash_id, page = callback.data.split(":")
    trash_id, page = int(trash_id), int(page)
    lang = await get_user_language(callback.from_user.id)

    trash_item = await get_trash_by_id(trash_id)
    name = trash_item.name if trash_item else ""

    restored = await restore_trash_customer(trash_id)
    if restored:
        await callback.answer(get_text("customer_restored", lang, name=name), show_alert=True)

    trash_items, total, page, total_pages = await get_trash_list(page=page)
    if not trash_items and page > 1:
        trash_items, total, page, total_pages = await get_trash_list(page=page - 1)

    if not trash_items:
        await callback.message.edit_text(get_text("no_trash", lang))
        return

    text = get_text("trash_list_title", lang, total=total)
    keyboard = get_trash_list_keyboard(trash_items, page, total_pages, lang)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("hard_delete_trash:"))
async def hard_delete_trash_callback(callback: CallbackQuery):
    _, trash_id, page = callback.data.split(":")
    trash_id, page = int(trash_id), int(page)
    lang = await get_user_language(callback.from_user.id)

    deleted = await hard_delete_trash_customer(trash_id)
    if deleted:
        await callback.answer(get_text("customer_hard_deleted", lang), show_alert=True)

    trash_items, total, page, total_pages = await get_trash_list(page=page)
    if not trash_items and page > 1:
        trash_items, total, page, total_pages = await get_trash_list(page=page - 1)

    if not trash_items:
        await callback.message.edit_text(get_text("no_trash", lang))
        return

    text = get_text("trash_list_title", lang, total=total)
    keyboard = get_trash_list_keyboard(trash_items, page, total_pages, lang)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
