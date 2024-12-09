from aiogram.filters import BaseFilter
from aiogram.types import Message

import local_settings as st
from database import check_admin, check_student


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        data = await check_admin(message.from_user.id)
        if  data is not None:
            message.model_config["filter_result"] = data
            return True
        else:
            return False
        

class IsStudent(BaseFilter):

    async def __call__(self, message: Message):
        data = await check_student(message.from_user.id)
        if data is not None:
            message.model_config["filter_result"] = data
            return True
        else:
            return False