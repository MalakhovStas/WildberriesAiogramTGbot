import time
from collections import namedtuple
from typing import Dict

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, CallbackQuery, Update

from config_data.bot_messages import BotSays
from config_data.config import LIMITED_TIME, ANTIFLOOD_TIME
from loader import bot, logger, dbase, storage
from utils.decorators import exception_control


class AccessControlMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.users = {}
        self.__last_users_updates = {}

    @exception_control.func_exception_control  # access control
    async def on_pre_process_update(self, update: Update, data: Dict) -> None:
        """
        Проверяет права доступа пользователя к приложению записанные в базе данных, если доступ разрешен или
        пользователь не найден в базе, пропускает сообщение пользователя к дальнейшей обработке, также передаёт далее
        данные о пользователе полученные из базы данных, предварительно записав их в словарь data.
        """
        logger.debug(f'-> INCOMING -> update id: {update.update_id}')

        if update.message:
            is_update: Message = update.message

        elif update.callback_query:
            is_update: CallbackQuery = update.callback_query
        else:
            return

        user: namedtuple = dbase.select_user(update=is_update, user_id=is_update.from_user.id)
        self.users[is_update.from_user.id] = user

        if user:
            if user.access == 'denied' or user.access == 'block':
                logger.warning(f'-> BAD -> user access "denied" or "block" -> CancelHandler')
                raise CancelHandler()

            elif user.access == 'limited':
                now_date = time.time()

                if now_date - user.start_time_limited >= LIMITED_TIME:
                    dbase.update_user_access(update=is_update, user_id=is_update.from_user.id, access='allowed')

                else:
                    logger.debug(f'-> BAD -> user access is limited '
                                 f'for {(LIMITED_TIME - (now_date - user.start_time_limited)) // 1}'
                                 f' sec -> CancelHandler')
                    raise CancelHandler()

        else:
            if not (isinstance(is_update, Message) and is_update.text.startswith('/start')):
                await bot.send_message(chat_id=is_update.from_user.id, text='&#128073 /start')
                logger.debug(f'-> BAD -> the user has not activated the app -> CancelHandler')
                raise CancelHandler()

        logger.info(f'-> OK -> next -> middlewares -> flood control')
        return

    @exception_control.func_exception_control  # flood control
    async def on_process_update(self, update: Update, data: Dict) -> None:
        """ Контролирует время между сообщениями от пользователя для защиты от 'флуда' """

        logger.debug(f'-> INCOMING -> update id: {update.update_id}')

        now_date = time.time()  # С привязкой ко времени получения сообщения высокая точность
        # now_date = update.message.date.timestamp()  # С привязкой ко времени отправки сообщения точность - 1сек

        if update.message:
            is_update: Message = update.message
        elif update.callback_query:
            is_update: CallbackQuery = update.callback_query
        else:
            return

        if not is_update.from_user.id in self.__last_users_updates:
            self.__last_users_updates[is_update.from_user.id] = now_date, 0
            logger.debug(f'-> OK -> next -> middlewares -> state control')
            return

        else:
            time_last_update = self.__last_users_updates[is_update.from_user.id][0]
            num_flood = self.__last_users_updates[is_update.from_user.id][1]

            if now_date - time_last_update < ANTIFLOOD_TIME:
                if (isinstance(is_update, CallbackQuery) and num_flood > 3) \
                        or (isinstance(is_update, Message) and num_flood > 10):

                    dbase.update_user_access(update=is_update, user_id=is_update.from_user.id,
                                             access='limited', start_time_limited=now_date)

                    await bot.send_message(chat_id=is_update.from_user.id,
                                           text=BotSays.say('lot flooding',
                                                            file_name='flood_control') + f'{LIMITED_TIME // 60} мин')
                    del self.__last_users_updates[is_update.from_user.id]
                    raise CancelHandler()

                else:
                    if isinstance(is_update, Message):
                        await bot.delete_message(chat_id=is_update.chat.id, message_id=is_update.message_id)
                        if num_flood == 0:
                            await bot.send_message(chat_id=is_update.chat.id,
                                                   text=BotSays.say('too fast', file_name='flood_control'))
                        logger.warning(f'-> BAD -> user is flooding -> CancelHandler')

                    elif isinstance(is_update, CallbackQuery):
                        await bot.answer_callback_query(callback_query_id=is_update.id)
                        logger.warning(f'-> BAD -> user is flooding the keyboard-> CancelHandler')

                    self.__last_users_updates[is_update.from_user.id] = now_date, num_flood + 1
                    raise CancelHandler()

            else:
                self.__last_users_updates[is_update.from_user.id] = now_date, 0
                logger.debug(f'-> OK -> next -> middlewares -> state control')
                return

    @exception_control.func_exception_control  # state control message
    async def on_pre_process_message(self, update: Message, data: Dict) -> None:
        """
        Контролирует соответствие сообщений от пользователя его состоянию, в случае не соответствия
        отправляет пользователю сообщение и сбрасывает дальнейшую обработку сообщения.
        """
        logger.debug(f'-> INCOMING -> message: {update.text}')

        current_state = await FSMContext.get_state(FSMContext(storage=storage,
                                                              chat=update.from_user.id, user=update.from_user.id))
        user: namedtuple = self.users.pop(update.from_user.id)  # удаляет user из self.users если оставить -> .get

        if user and current_state and update.text.startswith('/start'):
            await bot.send_message(chat_id=update.chat.id,
                                   text=BotSays.say(file_name='state_control'))
            logger.debug(f'-> BAD -> the user did not complete the previous request -> CancelHandler')
            raise CancelHandler()

        data['data_from_middlewares'] = user
        await bot.send_chat_action(chat_id=update.from_user.id, action='typing')
        import handlers
        logger.debug(f'-> OK -> next -> message Handlers')

    @exception_control.func_exception_control  # state control callback_query
    async def on_pre_process_callback_query(self, update: CallbackQuery, data: Dict) -> None:
        """
        Контролирует соответствие нажатия инлайн кнопки пользователем его состоянию, в случае не соответствия
        отправляет пользователю сообщение и сбрасывает дальнейшую обработку коллбека.
        """
        logger.debug(f'-> INCOMING -> calback_query: {update.data}')

        current_state = await FSMContext.get_state(FSMContext(storage=storage,
                                                              chat=update.from_user.id, user=update.from_user.id))
        user: namedtuple = self.users.pop(update.from_user.id)  # удаляет user из self.users если оставить -> .get

        if user and \
                (current_state is None or not current_state in ('FSMCommonStates:first_keyboard',
                                                                'FSMCommonStates:second_keyboard')):
            await bot.answer_callback_query(callback_query_id=update.id,
                                            text=BotSays.old_keyboard(), show_alert=False)
            logger.debug(f'-> BAD -> keyboard does not match user state -> CancelHandler')
            raise CancelHandler()

        data['data_from_middlewares'] = user
        await bot.answer_callback_query(callback_query_id=update.id)
        import handlers
        logger.info(f'-> OK -> next -> callback_query Handlers')
