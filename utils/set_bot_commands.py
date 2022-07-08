from aiogram.types import BotCommand

from config_data.config import DEFAULT_COMMANDS


async def set_default_commands(bot):
    """Устанавливает команды в меню бота"""

    await bot.set_my_commands([BotCommand(command=item[0], description=item[1]) for item in DEFAULT_COMMANDS])
