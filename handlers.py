from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from datetime import datetime
from database import insert_student, get_all_admins, check_student, insert_assignment, select_assignment, get_assignment, insert_file_metadata, insert_submission, convert_file_name
from utils import StudentAddForm, AssignmentCreateForm, SubmitAssignmentForm
from keyboards import cancel_btn, submit_assignment_btn, submit_a_btn
from filters import validate_date, validate_time

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
    if validate_date(message.text):
        await state.update_data(due_date=message.text)
        await message.answer(text=f"Please enter due time 00:00. \nExample: {datetime.now().time().strftime('%H:%M')}", reply_markup=cancel_btn)
        await state.set_state(AssignmentCreateForm.due_time)
    else:
        await message.answer(text="Enter Valid date format")

async def get_time(message: Message, state: FSMContext):
    if validate_time(message.text):
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
    else:
        await message.answer(text="Enter Valid time format", reply_markup=ReplyKeyboardRemove())


async def submit_assignment(message: Message, state: FSMContext):
    assignments = await select_assignment(message.from_user.id)
    if len(assignments) > 0:
        for obj in assignments:
            await message.answer(text=f"{obj['title']}\n\nDue: {obj['due']}\n\nDescription:\n{obj['description']}", reply_markup=submit_assignment_btn(obj['_id']))
        await message.answer(text="Choose assignment to submit")
    else:
        await message.answer(text="No Assignments")

async def submit_callback(call: CallbackQuery, bot: Bot, state: FSMContext):
    a_id = call.data.split('_')[1]
    await state.update_data({'submit_id': a_id})
    print('callback', a_id)
    await state.set_state(SubmitAssignmentForm.file)
    await call.message.answer('Submit your file', reply_markup=cancel_btn)
    await call.answer() 

async def get_file(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    a_id = data['submit_id']
    student = await check_student(message.from_user.id)
    assignment = await get_assignment(a_id)

    try:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        local_file_path = await convert_file_name(message.document.file_name)

        await bot.download_file(file_path, local_file_path)

         # Save file metadata to MongoDB
        file_metadata = {
            "file_name": message.document.file_name,
            "file_size": message.document.file_size,
            "file_id": file_id,
            "user_id": message.from_user.id,
            "local_path": local_file_path
        }

        metadata_saved = await insert_file_metadata(file_metadata)

        if metadata_saved:
            submission = {
                'assignment': assignment,
                'student': student,
                'file': file_metadata,
                'submitted_at': datetime.now()
            }
            submitted = await insert_submission(submission)

            chats = await get_all_admins()
            for admin in chats:
                await bot.send_message(text=f"Student: {student['name']} submitted assignment: {assignment['title']}", chat_id=admin['tgid'])
                await bot.send_document(document=file_id, chat_id=admin['tgid'])

            await message.reply(f"File submitted successfully", reply_markup=submit_a_btn)
            await state.clear()
        else: 
            await message.reply(f"An error occurred")
        
    except Exception as e:
        await message.reply(f"An error occurred: {e}")