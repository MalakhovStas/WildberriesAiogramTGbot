from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from config_data.config import SUPPORT
from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
async def func_keyboard(update: CallbackQuery | Message) -> InlineKeyboardMarkup:
    """ Создает и возвращает клавиатуру с двумя кнопками "Проверить ещё" и "Поддержка", в callback
        ключи для handler """

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text='Проверить ещё', callback_data='check_more'))
    keyboard.insert(InlineKeyboardButton(text='Поддержка', callback_data='send_support', url='https://t.me/' + SUPPORT))

    logger.debug(f'-> OK -> return keyboard')
    return keyboard
