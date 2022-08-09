import random
import time
from typing import Dict

from aiogram.types import Message, CallbackQuery

from config_data.config import UA_and_PROXIES, TIME_QUARANTINE_PROXI
from utils.decorators import exception_control
from utils.misc.admins_send_message import func_admins_message


@exception_control.func_exception_control
async def func_rotation(update: CallbackQuery | Message | None, bad_proxi: Dict | None = None,
                        stop_proxies={}) -> tuple:
    """
    Модуль для ротации и карантина прокси, если при вызове функции указан bad_proxi он попадает в карантин на срок,
    указанный в переменной TIME_CARANTIN_PROXI в секундах.
    """
    for tm, pr in stop_proxies.items():
        if time.time() - tm >= TIME_QUARANTINE_PROXI:
            stop_proxies.pop(tm)

    if bad_proxi:
        stop_proxies[time.time()] = bad_proxi
        await func_admins_message(update=update, message=f'&#9888 <b>WARNING Message to admins</b> &#9888\n'
                                                         f'<b>Proxi</b>: {bad_proxi} <b>is quarantined</b>\n'
                                                         f'<b>Num proxies in quarantined</b>: {len(stop_proxies)}'
                                                         f'<b>File:</b> proxi_rotation.py', exc=True)

    if len(stop_proxies) >= len(UA_and_PROXIES):
        await func_admins_message(update=update, message=f'&#9888 <b>WARNING Message to admins</b> &#9888\n'
                                                         f'&#9888 <b>!!! All proxies in quarantined !!!</b> &#9888\n'
                                                         f'<b>File:</b> proxi_rotation.py', exc=True)
        return '', ''

    while True:
        user_agent = random.choice(list(UA_and_PROXIES.keys()))
        proxi = UA_and_PROXIES[user_agent]
        if proxi not in stop_proxies.values():
            return user_agent, proxi
