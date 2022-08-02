from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from config_data.bot_messages import BotSays
from loader import dp, bot, logger, dbase
from states.states import FSMCommonStates
from utils.decorators import exception_control


@dp.callback_query_handler(state=FSMCommonStates.first_keyboard)
@exception_control.func_exception_control
async def func_get_first_keyboard(call: CallbackQuery, state: FSMContext, data_from_middlewares) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры "first_keyboard", отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), изменяет состояние пользователя.
    """
    logger.debug(f'-> INCOMING -> callback from first keyboard {call.data}')

    # Поменял на удаление, так лучше
    # await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
    #                                     reply_markup=None)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    if data_from_middlewares.balance_requests > 0:
        dbase.minus_from_balance_requests(update=call, user_id=call.from_user.id)

        if call.data == 'searching':
            await bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('searching'))
            await state.set_state(state=FSMCommonStates.searching_request)
            logger.debug(f'-> OK -> next state -> searching_request')

        elif call.data == 'card':
            await bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('card'))
            await state.set_state(state=FSMCommonStates.card_request)
            logger.debug(f'-> OK -> next state -> card_request')
    else:
        await state.reset_state()
        await bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('not_balance'))
        logger.debug(f'-> BAD -> reset state -> not balance requests')
