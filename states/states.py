from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMCommonStates(StatesGroup):
    """ Класс общих состояний """

    first_keyboard = State()
    searching_request = State()
    card_request = State()
    second_keyboard = State()


class FSMAdminStates(StatesGroup):
    """ Класс состояний администратора """

    password_mailing = State()
    mailing = State()


class FSMClientStates(StatesGroup):
    """Класс состояний клиентов"""
    pass