from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


# Эта клавиатура сейчас в проекте не используется
@exception_control.func_exception_control
async def func_keyboard(update: CallbackQuery | Message) -> ReplyKeyboardMarkup:
    """ Создает и возвращает клавиатуру с двумя кнопками "Реклама в поиске" и "Реклама в карточке", в callback
        ключи для handler """

    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Реклама в поиске', callback_data='searching'))
    keyboard.insert(KeyboardButton(text='Реклама в карточке', callback_data='card'))

    logger.debug(f'-> OK -> return keyboard')
    return keyboard
