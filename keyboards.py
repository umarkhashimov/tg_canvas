from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Mening ismim"),
        KeyboardButton(text="Jo'natish"),
    ],
    
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Choose btn', selective=True)
