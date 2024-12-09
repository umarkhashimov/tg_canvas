from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description="About bot"),
        BotCommand(command='group_create', description="Create new group"),
        BotCommand(command='student_add', description="Add new student"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())