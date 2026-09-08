from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.messages import get_text
from bot.keyboards import get_main_keyboard, get_auth_keyboard, get_cancel_keyboard
from bot.states import LoginState
from bot.services import (
    get_user_language,
    authenticate_and_login_user,
    logout_telegram_user,
)

router = Router()


@router.message(F.text.in_(["🔑 Tizimga kirish", "🔑 Войти в систему"]))
@router.message(Command("login"))
async def login_start_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    await state.set_state(LoginState.username)
    await message.answer(
        text=get_text("enter_username", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(LoginState.username)
async def login_username_step(message: Message, state: FSMContext):
    username = message.text.strip()
    await state.update_data(username=username)
    lang = await get_user_language(message.from_user.id)
    await state.set_state(LoginState.password)
    await message.answer(
        text=get_text("enter_password", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(LoginState.password)
async def login_password_step(message: Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    username = data.get("username")
    lang = await get_user_language(message.from_user.id)
    await state.clear()

    # Xavfsizlik uchun foydalanuvchining parol xabarini o'chiramiz
    try:
        await message.delete()
    except Exception:
        pass

    django_user = await authenticate_and_login_user(
        telegram_id=message.from_user.id,
        username_input=username,
        password_input=password
    )

    if django_user is not None:
        user_name = django_user.get_full_name() or django_user.username
        success_text = get_text("login_success", lang, user_name=user_name)
        await message.answer(
            text=success_text,
            reply_markup=get_main_keyboard(lang),
            parse_mode="HTML"
        )
    else:
        fail_text = get_text("login_failed", lang)
        await message.answer(
            text=fail_text,
            reply_markup=get_auth_keyboard(lang),
            parse_mode="HTML"
        )


@router.message(F.text.in_(["🚪 Chiqish", "🚪 Выйти"]))
@router.message(Command("logout"))
async def logout_handler(message: Message, state: FSMContext):
    await state.clear()
    await logout_telegram_user(message.from_user.id)
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=get_text("logged_out", lang),
        reply_markup=get_auth_keyboard(lang),
        parse_mode="HTML"
    )
