from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from database import check_admin


async def set_commands(bot: Bot, tgid):
    
    public_commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description="About bot"),
    ]
    await bot.set_my_commands(commands=public_commands, scope=BotCommandScopeDefault())

    admin_commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description="About bot"),
        BotCommand(command='group_create', description="Create new group"),
        BotCommand(command='student_add', description="Add new student"),
    ]

    if await check_admin(tgid):
        await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=tgid))
