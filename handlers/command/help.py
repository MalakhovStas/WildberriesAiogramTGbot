from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config_data.bot_messages import BotSays
from keyboards import first_keyboard
from loader import dp, bot, logger
from states.states import FSMCommonStates
from utils.decorators import exception_control


@dp.message_handler(commands=['help'], state='*')
@exception_control.func_exception_control
async def func_help(message: Message, state: FSMContext) -> None:
    """ Обработчик команды(help), отправляет пользователю объяснение работы бота и ссылку на чат поддержки."""

    logger.info(f'-> INCOMING -> command: {message.text}')
    keyboard = await first_keyboard.func_keyboard(update=message)
    await bot.send_message(
        chat_id=message.chat.id, text=BotSays.say('user', file_name='start.py'), reply_markup=keyboard)
    await state.set_state(state=FSMCommonStates.first_keyboard)
    logger.debug(f'-> OK -> send help -> next state -> first_keyboard')
