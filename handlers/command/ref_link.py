from aiogram.types import Message

from config_data.config import BOT_NIKNAME
from loader import dp, bot, logger
from utils.decorators import exception_control


@dp.message_handler(commands=['ref_link'], state='*')
@exception_control.func_exception_control
async def func_help(message: Message) -> None:
    """ Обработчик команды(ref_link), отправляет пользователю реферальную ссылку"""
    logger.debug(f'-> INCOMING -> command: {message.text}')
    await bot.send_message(chat_id=message.chat.id, text=f'https://t.me/{BOT_NIKNAME}?start={message.from_user.id}',
                           disable_web_page_preview=True)
    logger.debug(f'-> OK -> send referal link')
