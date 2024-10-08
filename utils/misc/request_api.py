import json
from typing import List, Dict

import requests
from aiogram.types import Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control
from utils.misc.admins_send_message import func_admins_message
from utils.misc.proxi_rotation import func_rotation


@exception_control.func_exception_control
async def func_request(url: str, update: CallbackQuery | Message | None) -> Dict | List:
    """ Запрашивает данные с API сайта(url), в случае успеха возвращает полученное сообщение в виде словаря или списка,
        в противном случае возвращает пустой словарь и отправляет сообщение об ошибке запроса администраторам """

    user_agent, proxi = await func_rotation(update=update)

    for step in range(1, 4):
        if step > 1:
            user_agent, proxi = await func_rotation(update=update, bad_proxi=proxi)

        response_api = requests.get(url=url, headers={'User-Agent': user_agent}, proxies=proxi)

        if response_api.status_code == requests.codes.ok and response_api.text:
            logger.debug(f'-> OK -> return -> response_api in json')
            return json.loads(response_api.text)

        else:
            logger.warning(f'-> BAD -> response -> status code: {response_api.status_code} -> '
                           f'text: {response_api.text} -> return -> None')
            await func_admins_message(update=update,
                                      message=f'&#9888 <b>WARNING Message to admins</b> &#9888\n'
                                              f'<b>File:</b> request_api.py\n'
                                              f'<b>Request to URL:</b> {url}\n'
                                              f'<b>Response API status code:</b> {response_api.status_code}\n'
                                              f'<b>Bad proxi:</b> {proxi}'
                                              f'<b>Response API text:</b> {response_api.text} -> '
                                              f'return -> None', exc=True)
    return dict()
