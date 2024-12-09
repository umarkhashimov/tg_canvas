import asyncio
# import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import local_settings as st
import handlers
import filters

async def start_notify(bot: Bot):
    for uid in st.ADMIN_LIST:
        await bot.send_message(uid, text='Bot started')

async def stop_notify(bot: Bot):
    for uid in st.ADMIN_LIST:
        await bot.send_message(uid, text='Bot stopped')

async def greet_admin(message: Message, bot: Bot):
    await message.answer(text="Welcome Admin")

async def start():
    # logging.basicConfig(level=logging.INFO)
    bot = Bot(token=st.TOKEN)
    dp = Dispatcher()

    
    # dp.startup.register(start_notify)
    # dp.shutdown.register(stop_notify)
    # dp.message.register(greet, CommandStart)
    dp.message.register(greet_admin, CommandStart(), filters.IsAdmin())
    dp.message.register(handlers.greet, CommandStart(), filters.IsStudent())


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())