import asyncio
# import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import local_settings as st
import handlers
import filters
from commands import set_commands, CancelCommand, SubmitCommand
from utils import StudentAddForm, AssignmentCreateForm as AForm, SubmitAssignmentForm as SubmitForm
from database import default_admins
from keyboards import submit_a_btn


bot = Bot(token=st.TOKEN)
async def start_notify(bot: Bot):
    for uid in st.DEFAULT_ADMINS:
        await bot.send_message(uid, text='Bot started')

async def stop_notify(bot: Bot):
    for uid in st.DEFAULT_ADMINS:
        await bot.send_message(uid, text='Bot stopped')

async def greet_admin(message: Message, bot: Bot):
    await set_commands(bot)
    data = message.model_config.get("filter_result")
    await message.answer(f"Welcome admin {data['name']}")

async def greet(message: Message):
    await set_commands(bot)
    data = message.model_config.get("filter_result")
    await message.answer(f"Welcome {data['name']}", reply_markup=submit_a_btn)

async def start():
    # logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    await default_admins()
    await set_commands(bot)
    
    # dp.startup.register(start_notify)
    # dp.shutdown.register(stop_notify)
    dp.message.register(greet_admin, CommandStart(), filters.IsAdmin())
    dp.message.register(greet, CommandStart(), filters.IsStudent())

    dp.message.register(handlers.cancel_action, CancelCommand(), F.text)
    dp.message.register(handlers.submit_assignment, filters.IsStudent(), SubmitCommand(), F.text)
    dp.message.register(handlers.create_assignment, filters.IsAdmin(), Command('create_assignment'))
    dp.message.register(handlers.add_student, filters.IsAdmin(), Command('student_add'))
    dp.message.register(handlers.get_name,  F.text, filters.IsAdmin(), StudentAddForm.name)
    dp.message.register(handlers.get_tgid,  F.text, filters.IsAdmin(), StudentAddForm.tgid)

    dp.message.register(handlers.get_title, F.text, filters.IsAdmin(), AForm.title)
    dp.message.register(handlers.get_descrition, F.text, filters.IsAdmin(), AForm.description)
    dp.message.register(handlers.get_date, F.text, filters.IsAdmin(), AForm.due_date)
    dp.message.register(handlers.get_time, F.text, filters.IsAdmin(), AForm.due_time)

    dp.message.register(handlers.get_file, F.document, filters.IsStudent(), SubmitForm.file)
    dp.callback_query.register(handlers.submit_callback, filters.IsStudent())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())