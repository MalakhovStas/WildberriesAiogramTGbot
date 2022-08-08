import sqlite3
from collections import namedtuple

from aiogram.types import Message, CallbackQuery

from config_data import config
from loader import logger
# from utils.decorators import exception_control


class Database:
    """Класс описывающий работу приложения с базой данных"""

    def __init__(self, path_db):
        self.database = sqlite3.connect(path_db)
        self.cursor = self.database.cursor()

    def create_table(self) -> None:
        with self.database:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                                    user_id INTEGER PRIMARY KEY NOT NULL,
                                    name TEXT,
                                    username TEXT,
                                    referer_id INTEGER,
                                    balance_requests INTEGER NOT NULL DEFAULT 10,
                                    access TEXT, 
                                    start_time_limited INTEGER,
                                    position TEXT,
                                    password TEXT)""")
            self.database.commit()
        logger.debug(f'-> OK -> CREATE TABLE "user" IF NOT EXISTS in database "{config.BD_DATABASE}"')

    # @exception_control.func_exception_control
    def insert_user(self, update: Message | CallbackQuery, user_id: int, name: str, access: str, username: str,
                    referer_id: int | None, balance_requests: int, start_time_limited: int | None = None,
                    position: str | None = None, password: str | None = None) -> None:
        with self.database:
            self.cursor.execute("INSERT INTO users(user_id, name, username, referer_id, balance_requests, access, "
                                "start_time_limited, position, password) VALUES "
                                "(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, name, username, referer_id,
                                                                balance_requests, access, start_time_limited, position,
                                                                password))
            self.database.commit()
        logger.debug(f'-> OK -> INSERT new user -> user_id: {user_id} name: {name}')

    # @exception_control.func_exception_control
    def update_user_access(self, update: Message | CallbackQuery, user_id: int, access: str,
                           start_time_limited: float | None = None) -> None:
        with self.database:
            self.cursor.execute("UPDATE users SET access = ?, start_time_limited = ? WHERE user_id = ?",
                                (access, start_time_limited, user_id))
            self.database.commit()
        logger.debug(f'-> OK -> UPDATE user -> user_id: {user_id} access: {access}')

    # @exception_control.func_exception_control
    def add_to_balance_requests(self, update: Message | CallbackQuery, user_id: int, add_to_balance: int) -> None:
        with self.database:
            self.cursor.execute("UPDATE users SET balance_requests = balance_requests + ? WHERE user_id = ?",
                                (add_to_balance, user_id))
            self.database.commit()
        logger.debug(f'-> OK -> UPDATE user -> user_id: {user_id} add_to_balance_requests: {add_to_balance}')

    # @exception_control.func_exception_control
    def minus_from_balance_requests(self, update: Message | CallbackQuery, user_id: int,
                                    minus_from_balance: int = 1) -> None:
        with self.database:
            self.cursor.execute("UPDATE users SET balance_requests = balance_requests - ? WHERE user_id = ?",
                                (minus_from_balance, user_id))
            self.database.commit()
        logger.debug(f'-> OK -> UPDATE user -> user_id: {user_id} minus_from_balance_requests: {minus_from_balance}')

    # @exception_control.func_exception_control
    def count_referals(self, update: Message | CallbackQuery, user_id: int) -> int:
        with self.database:
            count = self.cursor.execute("SELECT COUNT('user_id') FROM 'users' WHERE 'referer_id' = ?",
                                        (user_id,)).fetchone()[0]
        logger.debug(f'-> OK -> COUNT referal users -> {count}')
        return count

    # @exception_control.func_exception_control
    def select_user(self, update: Message | CallbackQuery, user_id: int) -> namedtuple:
        user = namedtuple('user', ['user_id', 'name', 'username', 'position', 'password', 'referer_id',
                                   'balance_requests', 'access', 'start_time_limited'])
        with self.database:
            self.cursor.execute("SELECT user_id, name, username, position, password, referer_id, balance_requests, "
                                "access, start_time_limited FROM users WHERE user_id = ?", (user_id,))
            data = self.cursor.fetchone()
        if data:
            user = user(*data)
        else:
            user = None
        logger.debug(f'-> OK -> SELECT user -> return -> {user}')
        return user

    # @exception_control.func_exception_control
    def select_all_users(self, update: Message | CallbackQuery, only_len: bool = False) -> tuple | int:
        with self.database:
            self.cursor.execute("SELECT user_id FROM users")
            users = tuple(user[0] for user in self.cursor.fetchall())

        if not users:
            logger.error(f'-> BAD -> NOT users in database -> return -> empty tuple')
            return tuple() if not only_len else 0
        else:
            logger.debug(f'-> OK -> SELECT all users -> return -> {len(users)} user_id')
            return users if not only_len else len(users)

    # @exception_control.func_exception_control
    def select_password(self, update: Message | CallbackQuery, user_id: int) -> str:
        with self.database:
            self.cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
            password = self.cursor.fetchone()
        logger.debug(f'-> OK -> SELECT password {password}')
        return ''.join(password)


#TODO сделать базу данных для аналитики активности пользователей - сначала разработать модель
    # def create_admin_info_table(self) -> None:
    #     with self.database:
    #         self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin_info(
    #                                 user_id INTEGER PRIMARY KEY NOT NULL,
    #                                 name TEXT,
    #                                 username TEXT,
    #                                 referer_id INTEGER,
    #                                 balance_requests INTEGER NOT NULL DEFAULT 10,
    #                                 access TEXT,
    #                                 start_time_limited INTEGER,
    #                                 position TEXT,
    #                                 password TEXT)""")
    #         self.database.commit()
    #     logger.debug(f'-> OK -> CREATE TABLE "user" IF NOT EXISTS in database "{config.BD_DATABASE}"')