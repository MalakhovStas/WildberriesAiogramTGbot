import functools
from typing import Callable, Any

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery, Message, Update
from aiogram.utils.exceptions import TelegramAPIError

from loader import logger, storage


def func_exception_control(func: Callable) -> Callable:
    """
    Декоратор, контролирует выполнение кода в функции, в случае успешного выполнения возвращает результат
    выполнения функции, в случае исключения вызывает функцию reset.func_reset для сброса состояния пользователя
    и возвращает None.
    """

    @functools.wraps(func)
    async def wrapped_func(*args, **kwargs) -> Any | None:
        try:
            result = await func(*args, **kwargs)
            return result

        except BaseException as exc:
            if isinstance(exc, CancelHandler):
                raise CancelHandler()
            try:
                arg = [arg for arg in args if isinstance(arg, (Message, CallbackQuery, Update))]
                if arg:
                    update: Message | CallbackQuery | Update = arg[0]

                    if isinstance(update, Update):  # Проверка для middelwares
                        if update.message:
                            update = update.message
                        elif update.callback_query:
                            update = update.callback_query

                else:
                    update: Message | CallbackQuery = kwargs.get('update')

                if not exc.__class__ == TelegramAPIError:

                    from utils.misc import admins_send_message
                    await admins_send_message.func_admins_message(update=update, exc=exc)

                    if not func.__name__ == 'func_reset':
                        from handlers.command import reset
                        await reset.func_reset(update=update,
                                               state=FSMContext(storage=storage,
                                                                chat=update.from_user.id,
                                                                user=update.from_user.id), error=True)
                else:
                    logger.error(f'-> ERROR -> Exception: {exc.__class__.__name__} -> Traceback: {exc} -> '
                                 f'User_name: {update.from_user.first_name} '
                                 f'User_id: {update.from_user.id}')
                return None
            except BaseException as exc:
                logger.exception(exc)

    return wrapped_func
