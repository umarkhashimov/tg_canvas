from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

cancel_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Cancel"),
    ],
    
], resize_keyboard=True, one_time_keyboard=True, selective=True)
