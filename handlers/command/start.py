import time

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config_data import bot_messages, config
from config_data.config import ADMINS, TECH_ADMINS, DEFAULT_ADMINS_PASSWORD
from keyboards import first_keyboard
from loader import bot, logger, dp, dbase
from states.states import FSMCommonStates
from utils.decorators import exception_control
from utils.misc import referal_system


@dp.message_handler(commands=['start'], state=None)
@exception_control.func_exception_control
async def start(message: Message, state: FSMContext, data_from_middlewares) -> None:
    """
    Обработчик команды /start, если пользователь не найден в базе данных, записывает его, таким образом
    запускает процесс взаимодействия бота с пользователем.
    """
    logger.debug(f'-> INCOMING -> command: {message.text}')

    keyboard = await first_keyboard.func_keyboard(update=message)

    await bot.send_message(chat_id=message.chat.id, text=f"&#129302")
    time.sleep(1.7)
    await bot.send_message(chat_id=message.chat.id, text=f"{bot_messages.BotSays.say('user')}", reply_markup=keyboard)

    if not data_from_middlewares:
        referer_id = message.text[7:] if len(message.text) > 7 else None
        if referer_id:
            if referer_id.isdigit() and len(referer_id) == 10 and referer_id != message.from_user.id:
                referer_id = int(referer_id)
                await referal_system.func_referal(update=message, referer_id=referer_id)
            else:
                referer_id = None
                logger.warning(f'-> BAD -> referer_id: {referer_id}')

        admins = tuple(map(int, ADMINS.split(', '))) if ADMINS else tuple()
        tech_admins = tuple(map(int, TECH_ADMINS.split(', '))) if TECH_ADMINS else tuple()

        if message.from_user.id in admins or tech_admins:
            position, password = 'admin', DEFAULT_ADMINS_PASSWORD
        else:
            position, password = None, None

        dbase.insert_user(update=message, user_id=message.from_user.id, name=message.from_user.full_name,
                          access='allowed', username=message.from_user.username, referer_id=referer_id,
                          balance_requests=config.START_BALANCE_REQUESTS, position=position, password=password)

        from utils.misc.admins_send_message import func_admins_message
        await func_admins_message(update=message, message=f'&#129395 <b>NEW USER</b>\n'
                                                          f'<b>User_ID:</b> {message.from_user.id}\n'
                                                          f'<b>User_name:</b> {message.from_user.full_name}\n')

        logger.info(f'-> NEW USER -> name: {message.from_user.full_name} , id: {message.from_user.id}')

    await state.set_state(state=FSMCommonStates.first_keyboard)
    logger.debug('-> OK -> next state -> first_keyboard')
