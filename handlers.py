from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from datetime import datetime
from database import insert_student, check_student, insert_assignment
from commands import set_commands
from utils import StudentAddForm, AssignmentCreateForm
from keyboards import cancel_btn

async def add_student(message: Message, state: FSMContext):
    await message.answer(text="Enter Student Full Name: ", reply_markup=cancel_btn)
    await state.set_state(StudentAddForm.name)

async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Enter telegram ID:", reply_markup=cancel_btn)
    await state.set_state(StudentAddForm.tgid)

async def get_tgid(message: Message, state: FSMContext):
    await state.update_data(tgid=message.text)
    await state.set_state(StudentAddForm.tgid)

    data = await state.get_data()

    if not await check_student(data['tgid']):

        if await insert_student(data):
            await message.answer(f"Student added.\nFull name: {data['name']}\nTelegram ID: {data['tgid']}")
        else:
            await message.answer(text='A problem Occured')
    else:
            await message.answer(text='Student with this Telegram ID already exists')

    await state.clear()


async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())


async def create_assignment(message: Message, state: FSMContext):
    await message.answer(text="Please enter assignment title.", reply_markup=cancel_btn)
    await state.set_state(AssignmentCreateForm.title)

async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text="Please enter assignment description.", reply_markup=cancel_btn)
    await state.set_state(AssignmentCreateForm.description)

async def get_descrition(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text=f"Please enter due date (d-m-y). \nExample: {datetime.today().strftime('%d-%m-%Y')}", reply_markup=cancel_btn)
    await state.set_state(AssignmentCreateForm.due_date)

async def get_date(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    await message.answer(text=f"Please enter due time 00:00. \nExample: {datetime.now().time().strftime('%H:%M')}", reply_markup=cancel_btn)
    await state.set_state(AssignmentCreateForm.due_time)

async def get_time(message: Message, state: FSMContext):
    await state.update_data(due_time=message.text)
    
    data = await state.get_data()
    datetime_obj = datetime.strptime(f"{data['due_date']} {data['due_time']}", "%d-%m-%Y %H:%M")

    assignment = {
        'title': data['title'],
        'description': data['description'],
        'due': datetime_obj
    }


    if await insert_assignment(assignment):
        await message.answer(f"Assignment created.\nTitle: {data['title']}\nDescription: {data['description']}\nDue: {datetime_obj}")
    else:
        await message.answer(text='A problem Occured')

    await state.clear()
    