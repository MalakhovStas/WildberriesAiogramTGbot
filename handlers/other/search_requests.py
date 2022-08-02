from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config_data import config
from loader import dp, logger, bot
from states.states import FSMCommonStates
from utils.decorators import exception_control
from utils.misc import request_api, response_request


@dp.message_handler(state=FSMCommonStates.searching_request, content_types=['text'])
@exception_control.func_exception_control
async def func_search(message: Message, state: FSMContext) -> None:
    """ Обработчик сообщения полученного в состоянии реклама в поиске, выделяет из сообщения номер карточки товара
        для запроса на API WB """

    logger.debug(f'-> INCOMING -> request: {message.text}')
    if message.text.strip().startswith('https:') or message.text.strip().isdigit():
        await bot.send_message(chat_id=message.chat.id,
                               text='&#129302 При запросе <b>"Реклама в поиске"</b> необходимо ввести'
                                    ' поисковый запрос, пример: <b>cвечи зажигания</b>\n'
                                    'Попробуйте ещё раз или сбросьте запрос &#128073 /reset')
    else:
        url = config.WB_CATALOG + '%20'.join(message.text.strip().split())

        response = await request_api.func_request(url=url, update=message)

        await response_request.func_response(message=message, state=state, response=response, url=url)
