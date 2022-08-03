from typing import Dict, List

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from config_data import config, bot_messages
from keyboards import second_keyboard
from loader import bot, logger
from states.states import FSMCommonStates
from utils.decorators import exception_control
from utils.misc import admins_send_message


@exception_control.func_exception_control
async def func_response(message: Message, state: FSMContext,
                        response: Dict | List, nmid: str = None, url: str = None) -> None:

    if isinstance(response, Dict):
        adverts = response.get('adverts')
        key_id = 'id'
    else:
        adverts = response
        key_id = 'nmId'
    keyboard = await second_keyboard.func_keyboard(update=message)

    # TODO разобраься ответ  WB есть но adverts - пустой список, как использовать другую информацию???
    # Запрос от user: нож охотничий с чехлом
    # Запрс к WB: https: // catalog - ads.wildberries.ru / api / v5 / search?keyword = нож%20охотничий%20с%20чехлом
    # # Вот такой ответ от WB
    # Ответ WB: {'pages': [{'positions': [1, 2, 11, 12, 14], 'page': 1, 'count': 5},
    #                {'positions': [1, 2, 13, 15, 18], 'page': 2, 'count': 5}],
    #                'prioritySubjects': [908, 811, 559, 2636, 1236], 'adverts': []}
    # print("адвертс:", adverts)
    # print("респонз:", response)

    if adverts and adverts != 'null':
        current_state = await state.get_state()
        line = '&#127760 Реальные ставки рекламы в\n'
        if current_state.endswith('card_request'):
            line += f"карточке товара по артикулу: " \
                   f"<b><i><a href='{config.LinkSTART}{nmid}{config.LinkEND}'>{nmid}</a></i></b>\n\n"

        elif current_state.endswith('searching_request'):
            line += f"поиске по запросу: <b><i>{message.text}</i></b>\n\n"

        for num, advert in enumerate(adverts):
            product_id = advert.get(key_id)
            cpm = str("{:,.0f}".format(advert.get('cpm')).replace(",", " "))
            emodji = f'&#{49 + num};&#65039;&#8419;' if num < 9 else '&#128287'
            line += f"{emodji} " \
                    f"Позиция <b><a href='{config.LinkSTART}" \
                    f"{product_id}{config.LinkEND}'>{product_id}</a></b> " \
                    f"Ставка <b>{cpm}</b> &#8381\n"
            if num == 9 or num == config.NUM_PROD - 1:
                break

        await bot.send_message(chat_id=message.from_user.id, text=line, reply_markup=keyboard)
        logger.debug('-> OK -> return adverts')

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=bot_messages.BotSays.say('not response'), reply_markup=keyboard)
        await admins_send_message.func_admins_message(update=message,
                                                      message=f'&#9888 <b>Некорректный запрос пользователя:</b>\n'
                                                              f'<b>ID:</b> {message.from_user.id}\n'
                                                              f'<b>Имя:</b> {message.from_user.first_name}\n'
                                                              f'<b>Контакт:</b> <a href="tg://user?id='
                                                              f'{message.from_user.id}">{message.from_user.username}'
                                                              f'</a>\n\n'
                                                              f'<b>Запрос от user:</b> {message.text}\n\n'
                                                              f'<b>Запрс к WB:</b> {url}\n\n'
                                                              f'<b>Ответ WB:</b> {response}', disable_preview_page=True)

        logger.warning('-> BAD -> return not response')

    await state.set_state(state=FSMCommonStates.second_keyboard)
    # await state.reset_state()
    logger.debug('-> next state -> second_keyboard')

