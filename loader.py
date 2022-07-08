from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from config_data import config
from database.database_utility_SQLite import Database

""" Модуль настройки загрузки и настройки основных инструментов приложения """

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)
dbase = Database(config.DATABASE_PATH)

logger.add(sink=config.LOGFILE_PATH, format=config.LOG_FORMAT, level=config.LOG_LEVEL, diagnose=True, backtrace=False,
           rotation="500 kb", retention=3, compression="zip")
