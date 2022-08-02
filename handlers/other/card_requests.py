import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config_data.config import WB_CAROUSEL
from loader import dp, logger, bot
from states.states import FSMCommonStates
from utils.decorators import exception_control
from utils.misc import request_api, response_request


@dp.message_handler(state=FSMCommonStates.card_request, content_types=['text'])
@exception_control.func_exception_control
async def func_card(message: Message, state: FSMContext) -> None:
    """ Обработчик сообщения полученного в состоянии реклама в карточке, выделяет из сообщения номер карточки товара для
        запроса на API WB """

    logger.debug(f'-> INCOMING -> request: {message.text}')

    if message.text.strip().isdigit() or message.text.strip().startswith('https:'):

        result = re.search(r'[^\/]{0,1}(\d+)[^\/]{0,1}', message.text)
        nmid = str(result.group(0)) if result else ''

        if not nmid:
            await bot.send_message(chat_id=message.chat.id,
                                   text='&#129302 Возможно указанная ссылка не соответствует ожидаемой, '
                                        'пример: https://www.wildberries.ru/catalog/39337945/detail.aspx\n'
                                        'также можно указать артикул товара, пример: <b>39337945</b>\n'
                                        'Попробуйте ещё раз или сбросьте запрос &#128073 /reset')
        else:
            response = await request_api.func_request(url=WB_CAROUSEL + nmid, update=message)

            await response_request.func_response(message=message, state=state, response=response, nmid=nmid,
                                                 url=WB_CAROUSEL + nmid)
    else:
        logger.debug(f'-> INCOMING -> request: {message.text}')
        await bot.send_message(chat_id=message.chat.id,
                               text='&#129302 При запросе <b>"Реклама в карточке"</b> необходимо ввести ссылку на товар'
                                    ', пример: https://www.wildberries.ru/catalog/39337945/detail.aspx\n'
                                    'или его артикул, пример: <b>39337945</b>\n'
                                    'Попробуйте ещё раз или сбросьте запрос &#128073 /reset')

    # https://www.wildberries.ru/catalog/25356409/detail.aspx
