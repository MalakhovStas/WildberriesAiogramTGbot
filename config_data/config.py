import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env\n'
         'Необходимо верно заполнить данные в файле .env.template и переименовать его в .env')
else:
    load_dotenv()

""" Уникальный ключ телеграмм бота -> загружается из файла .env """
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NIKNAME = os.getenv('BOT_NIKNAME')

""" Cписок администраторов и чат поддержки-> загружается из файла .env """
ADMINS = os.getenv('ADMINS')
TECH_ADMINS = os.getenv('TECH_ADMINS')

DEFAULT_ADMINS_PASSWORD = 'admin'
SUPPORT = os.getenv('SUPPORT')

""" Конфигурация БД """
DATABASE_PATH = r'database/database.db'  # для sqlite3

BD_USER = os.getenv('PSQL_USER')
BD_PASSWORD = os.getenv('PSQL_PASSWORD')
BD_DATABASE = os.getenv('PSQL_DATABASE')
BD_HOST = "127.0.0.1"
BD_PORT = "5432"

""" Параметры HTML запросов к API Wildberries """
WB_CATALOG = 'https://catalog-ads.wildberries.ru/api/v5/search?keyword='
WB_CAROUSEL = 'https://carousel-ads.wildberries.ru/api/v4/carousel?nm='
LinkSTART = 'https://www.wildberries.ru/catalog/'
LinkEND = '/detail.aspx'

""" Количество продуктов к выдаче пользователям """
NUM_PROD = 10

""" Начальный баланс разрешенных запросов пользователя """
START_BALANCE_REQUESTS = 30

""" Добавляет к балансу разрешенных запросов за каждого реферала """
ADD_TO_BALANCE_PER_REFERAL = 30

""" Количество рефералов для безлимитного доступа """
NUM_REFERALS_UNLIMIT = 3

""" Команды бота (также есть команда my_id в ответ возвращает id пользователя) """
DEFAULT_COMMANDS = (('start', 'запустить бота'),
                    ('help', 'написать в поддержку'),
                    ('reset', 'сбросить текущий запрос'),
                    ('ref_link', 'реферальная ссылка'),
                    )

""" Относительный путь к файлу с логами """
LOGFILE_PATH = 'log/debug.log'

""" Параметр уровня логирования """
LOG_LEVEL = 'DEBUG'

""" Формат логирования """
LOG_FORMAT = '{time:DD-MM-YYYY at HH:mm:ss} | {level: <8} | file: {file: ^30} | ' \
             'func: {function: ^30} | line: {line: >3} | message: {message}'

""" Время в секундах между сообщениями от пользователя, для контроля и защиты от 'флуда' """
ANTIFLOOD_TIME = 0.7

""" Время, временного ограничения доступа пользователя в секундах
   (устанавливается приложением автоматически, если пользователь флудит) """
LIMITED_TIME = 180

""" Максимальное количество попыток перезапуска бота в случае если он "упал" после ошибки """
MAX_RESTART_BOT = 5
