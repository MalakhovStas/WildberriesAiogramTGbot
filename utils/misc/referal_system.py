from aiogram.types import Message
from aiogram.utils.exceptions import TelegramAPIError

from config_data import config
from loader import bot, logger, dbase
from utils.decorators import exception_control


@exception_control.func_exception_control
async def func_referal(update: Message, referer_id: int) -> None:

    count_ref = dbase.count_referals(update=update, user_id=referer_id)

    try:
        if count_ref < config.NUM_REFERALS_UNLIMIT:
            dbase.add_to_balance_requests(update=update, user_id=referer_id,
                                          add_to_balance=config.ADD_TO_BALANCE_PER_REFERAL)
            await bot.send_message(chat_id=referer_id,
                                   text='&#129395 Новый пользователь по вашей ссылке\n'
                                        f'+ {config.ADD_TO_BALANCE_PER_REFERAL} к количеству доступных запросов')

        elif count_ref == config.NUM_REFERALS_UNLIMIT:
            dbase.add_to_balance_requests(update=update, user_id=referer_id, add_to_balance=config.MEGA_ADD_TO_BALANCE)
            await bot.send_message(chat_id=referer_id,
                                   text=f'&#129395 Новый пользователь по вашей ссылке &#129395\n'
                                        f'+ {config.MEGA_ADD_TO_BALANCE} к количеству доступных запросов, '
                                        f'теперь за каждого последующего реферала + {config.MEGA_ADD_TO_BALANCE}')
        else:
            dbase.add_to_balance_requests(update=update, user_id=referer_id, add_to_balance=config.MEGA_ADD_TO_BALANCE)
            await bot.send_message(chat_id=referer_id, text=f'&#129395 Новый пользователь по вашей ссылке\n'
                                                            f'их уже {count_ref}\n'
                                                            f'+ {config.MEGA_ADD_TO_BALANCE} '
                                                            f'к количеству доступных запросов')

        logger.info(f'-> NEW USER -> from referal link -> referer_id: {referer_id}')

    except TelegramAPIError:
        logger.warning(f'-> BAD -> referer_id: {referer_id} maybe blocked the bot')
