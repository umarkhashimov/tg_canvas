from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import insert_student, check_student
from commands import set_commands
from utils import StudentAddForm

async def add_student(message: Message, state: FSMContext):
    await message.answer(text="Enter Student Full Name: ")
    await state.set_state(StudentAddForm.name)

async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Save the name
    await message.answer("Enter telegram ID:")
    await state.set_state(StudentAddForm.tgid)

async def get_tgid(message: Message, state: FSMContext):
    await state.update_data(tgid=message.text)  # Save the name
    await state.set_state(StudentAddForm.tgid)

    data = await state.get_data()

    if not await check_student(data['tgid']):

        if await insert_student(data):
            await message.answer(f"Student added.\nFull name: {data['name']}\nTelegram ID: {data['tgid']}")
        else:
            await message.answer(text='A problem Occured')
    else:
            await message.answer(text='Student with this Telegram ID already exists')