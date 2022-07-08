import asyncio
import time

from art import tprint

from loader import bot, dp, logger, dbase
import middlewares
from utils.misc.admins_send_message import func_admins_message
from utils.set_bot_commands import set_default_commands


async def start(restart=0):
    """ Запуск бота, в случае 'падения' происходит перезапуск бота количество раз(MAX_RESTART_BOT), при: старте,
        рестарте и отключении бота отправляется сообщение администраторам """
    try:
        tprint('WBWorkBot')
        logger.info('-> START_BOT <-')
        await func_admins_message(message=f'&#128640 <b>START BOT</b> &#128640')

        await set_default_commands(bot)

        dbase.create_table()

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except BaseException as exc:
        logger.exception(exc)

        from config_data.config import MAX_RESTART_BOT
        await func_admins_message(message=f'&#9762&#9760 <b>BOT CRITICAL ERROR</b> &#9760&#9762\n<b>File</b>: main.py\n'
                                          f'<b>Exception</b>: {exc.__class__.__name__}\n'
                                          f'<b>Traceback</b>: {exc}', exc=True)

        if MAX_RESTART_BOT - restart:
            restart += 1
            await func_admins_message(message=f'&#9888<b>WARNING</b>&#9888\n'
                                              f'<b>10 seconds to {restart} restart BOT</b>!', exc=True)
            logger.info(f'-> 10seconds to {restart} restart BOT <-')
            time.sleep(10)

            await start(restart=restart)

        else:
            await func_admins_message(message=f'&#9760<b>BOT IS DEAD</b>&#9760')
            logger.critical('-> BOT IS DEAD <-')


if __name__ == '__main__':
    asyncio.run(start())
