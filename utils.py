from aiogram.fsm.state import State, StatesGroup

# Define states
class StudentAddForm(StatesGroup):
    name = State()
    tgid = State()


class AssignmentCreateForm(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    due_time = State()

# admins
# students