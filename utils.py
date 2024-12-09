from aiogram.fsm.state import State, StatesGroup

# Define states
class StudentAddForm(StatesGroup):
    name = State()
    tgid = State()
