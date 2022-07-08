from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
async def func_keyboard(update: CallbackQuery | Message) -> InlineKeyboardMarkup:
    """ Создает и возвращает клавиатуру с двумя кнопками "Реклама в поиске" и "Реклама в карточке", в callback
        ключи для handler """

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text='Реклама в поиске', callback_data='searching'))
    keyboard.insert(InlineKeyboardButton(text='Реклама в карточке', callback_data='card'))

    logger.debug(f'-> OK -> return keyboard')
    return keyboard
