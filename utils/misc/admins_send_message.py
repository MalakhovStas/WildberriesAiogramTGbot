import inspect
import time
from os.path import basename

from config_data.config import ADMINS, TECH_ADMINS
from loader import bot, logger


async def func_admins_message(update=None, exc=None, message=None, disable_preview_page=None):
    """Отправляет сообщения об ошибках и состоянии бота администраторам, если их id указаны в ADMINS."""

    try:
        if ADMINS or TECH_ADMINS:
            admins = tuple(map(int, ADMINS.split(', '))) if ADMINS else tuple()
            tech_admins = tuple(map(int, TECH_ADMINS.split(', '))) if TECH_ADMINS else tuple()
            if exc:
                if message:
                    for admin in tech_admins:
                        time.sleep(0.3)
                        await bot.send_message(chat_id=admin, text=message)
                else:
                    if len(inspect.trace()) > 1:
                        track = inspect.trace()[1]
                    else:
                        track = inspect.trace()[0]

                    file = basename(track.filename)
                    func = track.function
                    line = track.lineno
                    code = "".join(track.code_context)
                    logger.error(f'-> ERROR -> User_name: {update.from_user.first_name}, '
                                 f'User_id: {update.from_user.id} -> File: {file} -> Func: {func} -> Line: {line} -> '
                                 f'Exception: {exc.__class__.__name__} -> Traceback: {exc} -> Code: {code.strip()}')

                    for admin in tech_admins:
                        time.sleep(0.3)
                        await bot.send_message(chat_id=admin,
                                               text='&#9888 <b><i>ERROR</i></b> &#9888\n'
                                                    f'<b>User_name</b>:    {update.from_user.first_name}\n'
                                                    f'<b>User_id</b>:    {update.from_user.id}\n'
                                                    f'<b>File</b>:    <i>{file}</i>\n'
                                                    f'<b>Func</b>:    <i>{func}</i>\n'
                                                    f'<b>Line</b>:    {line}\n'
                                                    f'<b>Exception</b>:    {exc.__class__.__name__}\n'
                                                    f'<b>Traceback</b>:    {exc}\n'
                                                    f'<b>Code</b>:    {code.strip()}\n')

                        logger.info(f'-> ADMIN SEND MESSAGE -> ERROR -> admin_id: {admin}')

            elif message and exc is None:
                for admin in admins:
                    time.sleep(0.3)
                    await bot.send_message(chat_id=admin, text=message, disable_web_page_preview=disable_preview_page)
                    logger.info(f'-> ADMIN SEND MESSAGE -> admin_id: {admin}')

    except BaseException as i_exc:
        logger.exception(i_exc)
