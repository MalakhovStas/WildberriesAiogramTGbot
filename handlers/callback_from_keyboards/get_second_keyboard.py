from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from config_data.bot_messages import BotSays
from keyboards import first_keyboard
from loader import dp, bot, logger
from states.states import FSMCommonStates
from utils.decorators import exception_control


@dp.callback_query_handler(state=FSMCommonStates.second_keyboard)
@exception_control.func_exception_control
async def func_get_keyboard(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры "second_keyboard", отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), изменяет состояние пользователя.
    """
    logger.debug(f'-> INCOMING -> callback: {call.data}')

    # await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    if call.data == 'check_more':
        keyboard = await first_keyboard.func_keyboard(update=call)
        await bot.send_message(chat_id=call.from_user.id, text=BotSays.say('check_more'), reply_markup=keyboard)
        await state.set_state(state=FSMCommonStates.first_keyboard)
        logger.debug(f'-> OK -> next state -> searching_request')

    # это условие не работает
    elif call.data == 'send_support':
        await state.reset_state()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        logger.debug(f'-> OK -> return to support -> reset state')



