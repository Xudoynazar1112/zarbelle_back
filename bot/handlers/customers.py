from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import (
    get_main_keyboard,
    get_auth_keyboard,
    get_cancel_keyboard,
    get_skip_keyboard,
    get_yes_no_keyboard,
    get_customers_list_keyboard,
    get_customer_card_keyboard,
)
from bot.states import AddCustomerState, EditCommentState
from bot.services import (
    get_user_language,
    is_user_authenticated,
    get_customers_list,
    get_customer_by_id,
    create_customer,
    update_customer_comment,
    toggle_customer_field,
    delete_customer_to_trash,
)

router = Router()


# ---------------- BEKOR QILISH (CANCEL) ----------------
@router.message(F.text.in_(["❌ Bekor qilish", "❌ Отмена"]))
async def cancel_action_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    is_auth = await is_user_authenticated(message.from_user.id)
    keyboard = get_main_keyboard(lang) if is_auth else get_auth_keyboard(lang)
    await message.answer(
        text=get_text("action_cancelled", lang),
        reply_markup=keyboard
    )


# ---------------- NOOP / PAGE INFO CALLBACK ----------------
@router.callback_query(F.data == "noop")
@router.callback_query(F.data.startswith("page_info:"))
async def page_info_callback(callback: CallbackQuery):
    if ":" in callback.data:
        _, page, total_pages = callback.data.split(":")
        lang = await get_user_language(callback.from_user.id)
        info_text = f"📄 {page}-sahifa (Jami: {total_pages})" if lang == "uz" else f"📄 Страница {page} (Всего: {total_pages})"
        await callback.answer(info_text, show_alert=False)
    else:
        await callback.answer()


# ---------------- MIJOZLAR RO'YXATI (LIST) ----------------
@router.message(F.text.in_(["👥 Mijozlar ro'yxati", "👥 Список клиентов"]))
async def customers_list_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    if not await is_user_authenticated(message.from_user.id):
        await message.answer(get_text("auth_required", lang), reply_markup=get_auth_keyboard(lang), parse_mode="HTML")
        return

    customers, total, page, total_pages = await get_customers_list(page=1)

    if not customers:
        await message.answer(
            text=get_text("no_customers", lang),
            reply_markup=get_main_keyboard(lang)
        )
        return

    text = get_text("customers_list_title", lang, total=total)
    keyboard = get_customers_list_keyboard(customers, page, total_pages, lang)
    await message.answer(text=text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("customers_page:"))
async def customers_page_callback(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    lang = await get_user_language(callback.from_user.id)
    customers, total, page, total_pages = await get_customers_list(page=page)

    if not customers:
        await callback.message.edit_text(get_text("no_customers", lang))
        await callback.answer()
        return

    text = get_text("customers_list_title", lang, total=total)
    keyboard = get_customers_list_keyboard(customers, page, total_pages, lang)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


# ---------------- MIJOZ KARTASI (DETAIL) ----------------
@router.callback_query(F.data.startswith("view_customer:"))
async def view_customer_callback(callback: CallbackQuery):
    _, customer_id, page = callback.data.split(":")
    customer_id, page = int(customer_id), int(page)
    lang = await get_user_language(callback.from_user.id)
    customer = await get_customer_by_id(customer_id)

    if not customer:
        await callback.answer(get_text("no_customers", lang), show_alert=True)
        return

    connected_text = get_text("connected_yes", lang) if customer.is_connected else get_text("connected_no", lang)
    connected_icon = "✅" if customer.is_connected else "⏳"
    lead_text = get_text("lead_yes", lang) if customer.is_lead else get_text("lead_no", lang)
    lead_icon = "⭐️" if customer.is_lead else "⚪"
    comment_text = customer.comment if customer.comment else get_text("no_comment", lang)

    text = get_text(
        "customer_card",
        lang,
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        connected_icon=connected_icon,
        connected_text=connected_text,
        lead_icon=lead_icon,
        lead_text=lead_text,
        comment=comment_text,
        created_at=customer.created_at.strftime("%d.%m.%Y %H:%M") if customer.created_at else "-"
    )
    keyboard = get_customer_card_keyboard(customer.id, customer.is_connected, customer.is_lead, lang, page)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


# ---------------- STATUSLARNI O'ZGARTIRISH (TOGGLE) ----------------
@router.callback_query(F.data.startswith("toggle_connected:"))
async def toggle_connected_callback(callback: CallbackQuery):
    _, customer_id, page = callback.data.split(":")
    customer_id, page = int(customer_id), int(page)
    lang = await get_user_language(callback.from_user.id)

    customer = await toggle_customer_field(customer_id, "is_connected")
    if not customer:
        await callback.answer(get_text("no_customers", lang), show_alert=True)
        return

    connected_text = get_text("connected_yes", lang) if customer.is_connected else get_text("connected_no", lang)
    connected_icon = "✅" if customer.is_connected else "⏳"
    lead_text = get_text("lead_yes", lang) if customer.is_lead else get_text("lead_no", lang)
    lead_icon = "⭐️" if customer.is_lead else "⚪"
    comment_text = customer.comment if customer.comment else get_text("no_comment", lang)

    text = get_text(
        "customer_card",
        lang,
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        connected_icon=connected_icon,
        connected_text=connected_text,
        lead_icon=lead_icon,
        lead_text=lead_text,
        comment=comment_text,
        created_at=customer.created_at.strftime("%d.%m.%Y %H:%M") if customer.created_at else "-"
    )
    keyboard = get_customer_card_keyboard(customer.id, customer.is_connected, customer.is_lead, lang, page)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(get_text("status_updated", lang))


@router.callback_query(F.data.startswith("toggle_lead:"))
async def toggle_lead_callback(callback: CallbackQuery):
    _, customer_id, page = callback.data.split(":")
    customer_id, page = int(customer_id), int(page)
    lang = await get_user_language(callback.from_user.id)

    customer = await toggle_customer_field(customer_id, "is_lead")
    if not customer:
        await callback.answer(get_text("no_customers", lang), show_alert=True)
        return

    connected_text = get_text("connected_yes", lang) if customer.is_connected else get_text("connected_no", lang)
    connected_icon = "✅" if customer.is_connected else "⏳"
    lead_text = get_text("lead_yes", lang) if customer.is_lead else get_text("lead_no", lang)
    lead_icon = "⭐️" if customer.is_lead else "⚪"
    comment_text = customer.comment if customer.comment else get_text("no_comment", lang)

    text = get_text(
        "customer_card",
        lang,
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        connected_icon=connected_icon,
        connected_text=connected_text,
        lead_icon=lead_icon,
        lead_text=lead_text,
        comment=comment_text,
        created_at=customer.created_at.strftime("%d.%m.%Y %H:%M") if customer.created_at else "-"
    )
    keyboard = get_customer_card_keyboard(customer.id, customer.is_connected, customer.is_lead, lang, page)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(get_text("status_updated", lang))


# ---------------- IZOHNI TAHRIRLASH (EDIT COMMENT) ----------------
@router.callback_query(F.data.startswith("edit_comment:"))
async def edit_comment_start_callback(callback: CallbackQuery, state: FSMContext):
    _, customer_id, page = callback.data.split(":")
    customer_id, page = int(customer_id), int(page)
    lang = await get_user_language(callback.from_user.id)

    await state.set_state(EditCommentState.comment)
    await state.update_data(customer_id=customer_id, page=page)
    await callback.message.answer(
        text=get_text("enter_new_comment", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(EditCommentState.comment)
async def edit_comment_finish_step(message: Message, state: FSMContext):
    new_comment = message.text.strip()
    data = await state.get_data()
    customer_id = data.get("customer_id")
    page = data.get("page", 1)
    lang = await get_user_language(message.from_user.id)
    await state.clear()

    customer = await update_customer_comment(customer_id, new_comment)
    if customer:
        await message.answer(
            text=get_text("comment_updated", lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text=get_text("no_customers", lang),
            reply_markup=get_main_keyboard(lang)
        )


# ---------------- MIJOZNI O'CHIRISH (DELETE TO TRASH) ----------------
@router.callback_query(F.data.startswith("delete_customer:"))
async def delete_customer_callback(callback: CallbackQuery):
    _, customer_id, page = callback.data.split(":")
    customer_id, page = int(customer_id), int(page)
    lang = await get_user_language(callback.from_user.id)

    success = await delete_customer_to_trash(customer_id)
    if success:
        await callback.answer(get_text("customer_deleted", lang), show_alert=True)
    
    customers, total, page, total_pages = await get_customers_list(page=page)
    if not customers and page > 1:
        customers, total, page, total_pages = await get_customers_list(page=page - 1)

    if not customers:
        await callback.message.edit_text(get_text("no_customers", lang))
        return

    text = get_text("customers_list_title", lang, total=total)
    keyboard = get_customers_list_keyboard(customers, page, total_pages, lang)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")


# ---------------- YANGI MIJOZ QO'SHISH (FSM) ----------------
@router.message(F.text.in_(["➕ Yangi mijoz qo'shish", "➕ Добавить клиента"]))
async def add_customer_start(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    if not await is_user_authenticated(message.from_user.id):
        await message.answer(get_text("auth_required", lang), reply_markup=get_auth_keyboard(lang), parse_mode="HTML")
        return

    await state.set_state(AddCustomerState.name)
    await message.answer(
        text=get_text("enter_customer_name", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(AddCustomerState.name)
async def add_customer_name_step(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    lang = await get_user_language(message.from_user.id)
    await state.set_state(AddCustomerState.phone)
    await message.answer(
        text=get_text("enter_customer_phone", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(AddCustomerState.phone)
async def add_customer_phone_step(message: Message, state: FSMContext):
    phone = message.text.strip()
    await state.update_data(phone=phone)
    lang = await get_user_language(message.from_user.id)
    await state.set_state(AddCustomerState.is_connected)
    await message.answer(
        text=get_text("ask_is_connected", lang),
        reply_markup=get_yes_no_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(AddCustomerState.is_connected)
async def add_customer_connected_step(message: Message, state: FSMContext):
    text = message.text.strip()
    lang = await get_user_language(message.from_user.id)
    is_connected = True if ("Ha" in text or "Да" in text or "✅" in text) else False

    await state.update_data(is_connected=is_connected)
    await state.set_state(AddCustomerState.is_lead)
    await message.answer(
        text=get_text("ask_is_lead", lang),
        reply_markup=get_yes_no_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(AddCustomerState.is_lead)
async def add_customer_lead_step(message: Message, state: FSMContext):
    text = message.text.strip()
    lang = await get_user_language(message.from_user.id)
    is_lead = True if ("Ha" in text or "Да" in text or "✅" in text) else False

    await state.update_data(is_lead=is_lead)
    await state.set_state(AddCustomerState.comment)
    await message.answer(
        text=get_text("ask_comment", lang),
        reply_markup=get_skip_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(AddCustomerState.comment)
async def add_customer_comment_step(message: Message, state: FSMContext):
    text = message.text.strip()
    lang = await get_user_language(message.from_user.id)

    comment = None if ("O'tkazib yuborish" in text or "Пропустить" in text or "⏭️" in text) else text

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    is_connected = data.get("is_connected", False)
    is_lead = data.get("is_lead", False)

    await create_customer(
        name=name,
        phone=phone,
        is_connected=is_connected,
        is_lead=is_lead,
        comment=comment,
    )
    await state.clear()

    success_text = get_text("customer_added_success", lang, name=name, phone=phone)
    await message.answer(
        text=success_text,
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
