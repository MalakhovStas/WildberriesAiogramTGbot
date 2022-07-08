from aiogram.types import Message

from config_data.bot_messages import BotSays
from loader import dp, bot, logger
from utils.decorators import exception_control


@dp.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location',
                                   'contact'], state='*')
@exception_control.func_exception_control
async def func_any_message(message: Message) -> None:
    """Обработчик не текстовых данных полученных от пользователя, для реакции бота на сообщения."""

    logger.debug(f'-> INCOMING -> not text content: {message.content_type}')

    if message.content_type in ('audio', 'voice'):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('audio, voice'))

    elif message.content_type in ('document',):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('document'))

    elif message.content_type in ('video', 'video_note'):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('video'))

    elif message.content_type in ('photo',):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('photo'))

    elif message.content_type in ('sticker',):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('sticker'))

    elif message.content_type in ('location',):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('location'))

    elif message.content_type in ('contact',):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('contact'))
