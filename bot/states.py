from aiogram.fsm.state import State, StatesGroup


class LoginState(StatesGroup):
    username = State()
    password = State()


class AddCustomerState(StatesGroup):
    name = State()
    phone = State()
    is_connected = State()
    is_lead = State()
    comment = State()


class EditCommentState(StatesGroup):
    customer_id = State()
    page = State()
    comment = State()


class SearchCustomerState(StatesGroup):
    query = State()
