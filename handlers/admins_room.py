import time

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config_data.config import ADMINS, TECH_ADMINS
from loader import dp, bot, dbase, logger
from states.states import FSMAdminStates
from utils.decorators import exception_control


@dp.message_handler(commands=['my_id', 'mailing', 'commands', 'how_users'], state='*')
@exception_control.func_exception_control
async def admins_commands_handler(message: Message, state: FSMContext) -> None:
    command: str = message.get_command()
    admins = tuple(map(int, ADMINS.split(', '))) if ADMINS else tuple()
    tech_admins = tuple(map(int, TECH_ADMINS.split(', '))) if TECH_ADMINS else tuple()

    if message.from_user.id in admins or tech_admins:

        if command == '/commands':
            await AdminsHendlers.commands(update=message)

        elif command == '/my_id':
            await AdminsHendlers.my_id(update=message)

        elif command == '/how_users':
            num_users = dbase.select_all_users(update=message, only_len=True)
            await bot.send_message(chat_id=message.from_user.id, text=f'В базе: {num_users} пользователей')

        elif command == '/mailing':
            await bot.send_message(chat_id=message.from_user.id, text=f'Введите пароль:')
            await state.set_state(state=FSMAdminStates.password_mailing)


@dp.message_handler(state=FSMAdminStates.password_mailing)
@exception_control.func_exception_control
async def admins_in_password_handler(message: Message, state: FSMContext) -> None:
    await AdminsHendlers.in_password(update=message, state=state)


@dp.message_handler(state=FSMAdminStates.mailing)
@exception_control.func_exception_control
async def admins_mailing_handler(message: Message, state: FSMContext) -> None:
    await AdminsHendlers.mailing(update=message, state=state)


class AdminsHendlers:

    @staticmethod
    @exception_control.func_exception_control
    async def commands(update: Message) -> None:
        await bot.send_message(chat_id=update.chat.id, text=f'<b>Команды администратора:</b>\n'
                                                            f'<b>/commands</b> - список команд\n'
                                                            f'<b>/my_id</b> - мой id\n'
                                                            f'<b>/how_users</b> - кол-во пользователей в базе\n'
                                                            f'<b>/mailing</b> - рассылка пользователям бота\n')

    @staticmethod
    @exception_control.func_exception_control
    async def in_password(update: Message, state: FSMContext) -> None:
        password: str = dbase.select_password(update=update, user_id=update.from_user.id)
        current_state = await state.get_state()

        if not update.text == password:
            await bot.send_message(chat_id=update.chat.id, text=f'Пароль не верный.')
            await state.reset_state()
        else:

            # print(current_state, type(current_state))  # FSMAdminStates:password_mailing , str
            # print(current_state is FSMAdminStates.password_mailing)  # False
            # print(current_state == 'FSMAdminStates:password_mailing')  # True

            if current_state == 'FSMAdminStates:password_mailing':
                await bot.send_message(chat_id=update.chat.id, text=f'Введите сообщение для рассылки:')
                await state.set_state(state=FSMAdminStates.mailing)

    @staticmethod
    @exception_control.func_exception_control
    async def my_id(update: Message) -> None:
        await bot.send_message(chat_id=update.chat.id, text=f'Твой id: {update.from_user.id}')

    @staticmethod
    @exception_control.func_exception_control
    async def mailing(update: Message, state: FSMContext) -> None:
        num_send = 0
        id_users: tuple = dbase.select_all_users(update=update)

        await state.reset_state()
        for user_id in id_users:
            try:
                await bot.send_message(chat_id=user_id, text=f'{update.text}')
                num_send += 1
                time.sleep(0.3)
            except Exception as error:
                logger.error(f'-> BAD -> not send to user {user_id} error: {error}')
                continue

        await bot.send_message(chat_id=update.from_user.id, text=f'Отправлено: {num_send} из {len(id_users)}')
        logger.debug(f'-> OK -> send {num_send} out of {len(id_users)} users')
