import asyncio
# import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import local_settings as st
import handlers
import filters
from commands import set_commands, CancelCommand
from utils import StudentAddForm
from database import default_admins

bot = Bot(token=st.TOKEN)

async def start_notify(bot: Bot):
    for uid in st.DEFAULT_ADMINS:
        await bot.send_message(uid, text='Bot started')

async def stop_notify(bot: Bot):
    for uid in st.DEFAULT_ADMINS:
        await bot.send_message(uid, text='Bot stopped')

async def greet_admin(message: Message, bot: Bot):
    data = message.model_config.get("filter_result")
    await set_commands(bot=bot,tgid=message.from_user.id)
    await message.answer(f"Welcome admin {data['name']}")

async def greet(message: Message):
    data = message.model_config.get("filter_result")
    await set_commands(bot=bot,tgid=message.from_user.id)
    await message.answer(f"Welcome {data['name']}")

async def start():
    # logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    await default_admins()
    
    # dp.startup.register(start_notify)
    # dp.shutdown.register(stop_notify)
    dp.message.register(greet_admin, CommandStart(), filters.IsAdmin())
    dp.message.register(greet, CommandStart(), filters.IsStudent())

    dp.message.register(handlers.cancel_action, CancelCommand(), F.text)
    dp.message.register(handlers.add_student, filters.IsAdmin(), Command('student_add'))
    dp.message.register(handlers.get_name,  F.text, filters.IsAdmin(), StudentAddForm.name)
    dp.message.register(handlers.get_tgid,  F.text, filters.IsAdmin(), StudentAddForm.tgid)



    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())