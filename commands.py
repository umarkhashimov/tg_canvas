from aiogram import Bot
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from database import get_all_admins
from aiogram.filters import BaseFilter

async def set_commands(bot: Bot):
    public_commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description="About bot"),
    ]

    await bot.set_my_commands(commands=public_commands)

    admin_commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description="About bot"),
        BotCommand(command='group_create', description="Create new group"),
        BotCommand(command='create_assignment', description="Create new assignment"),
        BotCommand(command='student_add', description="Add new student"),
    ]

    chats = await get_all_admins()
    for obj in chats:
        await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=obj['tgid']))



class CancelCommand(BaseFilter):
    
    async def __call__(self, message: Message) -> bool:
        if message.text.lower() == "cancel":
            return True
        else:
            return False
        