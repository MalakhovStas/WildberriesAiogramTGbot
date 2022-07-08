from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from config_data.bot_messages import BotSays
from loader import bot, logger, dp
from utils.decorators import exception_control


@dp.message_handler(commands=['reset'], state='*')
@exception_control.func_exception_control
async def func_reset(update: Message | CallbackQuery, state: FSMContext, error: bool = False) -> None:
    """
    Обработчик команды /reset, сбрасывает состояние пользователя, также используется как функция сброса состояния
    в случае исключения в процессе обработки запроса от пользователя.
    """

    current_state = await state.get_state()

    if error:
        if current_state:

            await state.reset_state()
            await bot.send_message(chat_id=update.from_user.id, text=BotSays.say('error in state'))
            logger.debug(f'-> OK -> state reset')

        else:
            await bot.send_message(chat_id=update.from_user.id, text=BotSays.say('error state is None'))
    else:
        if current_state:
            await state.reset_state()
            await bot.send_message(chat_id=update.from_user.id, text=BotSays.say('not error in state'))
            logger.debug(f'-> OK -> state reset')

        else:
            await bot.send_message(chat_id=update.from_user.id, text=BotSays.say('not error state is None'))
