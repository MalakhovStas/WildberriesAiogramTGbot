from aiogram.types import Message

from config_data.bot_messages import BotSays
from loader import dp, bot, logger
from utils.decorators import exception_control


@dp.message_handler(commands=['help'], state='*')
@exception_control.func_exception_control
async def func_help(message: Message) -> None:
    """ Обработчик команды(help), отправляет пользователю объяснение работы бота и ссылку на чат поддержки."""

    logger.info(f'-> INCOMING -> command: {message.text}')
    await bot.send_message(chat_id=message.chat.id, text=BotSays.say('user', file_name='start.py'))
    logger.debug(f'-> OK -> send help')
