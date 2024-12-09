from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import  InlineKeyboardBuilder

cancel_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Cancel"),
    ],
    
], resize_keyboard=True, one_time_keyboard=True, selective=True)


submit_a_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Submit Assignment"),
    ],
    
], resize_keyboard=True, one_time_keyboard=True, selective=True)



def submit_assignment_btn(assignment_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Submmit", callback_data=f'submit_{assignment_id}')
    keyboard.adjust(1)

    return keyboard.as_markup()