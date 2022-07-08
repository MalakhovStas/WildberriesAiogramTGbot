from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config_data.bot_messages import BotSays
from keyboards import first_keyboard
from loader import dp, bot, logger
from states.states import FSMCommonStates
from utils.decorators import exception_control


@dp.message_handler(content_types=['text'], state='*')
@exception_control.func_exception_control
async def func_any_text(message: Message, state: FSMContext) -> None:
    """
    Обработчик текстовых сообщений, введенных с клавиатуры устройства пользователя, в любом состоянии
    пользователя, для реакции бота на сообщения.
    """
    logger.debug(f'-> INCOMING -> {message.text}')
    current_state = await state.get_state()

    if message.text.lower() in ('help', 'sos', 'помогите', 'спасите', 'нужна помощь', 'что делать', 'не понятно'):
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('user', file_name='start.py'))
        logger.debug(f'-> OK -> message to user -> start help')

    elif current_state is None:
        keyboard = await first_keyboard.func_keyboard(message)
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('state_is_none'), reply_markup=keyboard)
        await state.set_state(state=FSMCommonStates.first_keyboard)
        logger.debug(f'-> OK -> message to user -> state in none')

    elif current_state == 'FSMCommonStates:first_keyboard' or current_state == 'FSMCommonStates:second_keyboard':
        await bot.send_message(chat_id=message.chat.id, text=BotSays.say('keyboards'))
        logger.debug(f'-> OK -> message to user -> keyboards')
