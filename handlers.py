from aiogram.types import Message
from database import db

async def greet(message: Message):
    student = db['students'].find_one({'tg_id': str(message.from_user.id)})

    await message.answer(f"Welcome {student['name']}")




