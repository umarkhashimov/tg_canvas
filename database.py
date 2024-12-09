import local_settings as st
from pymongo import MongoClient

client = MongoClient(st.db_connection)
db = client[st.db_name]

async def check_admin(tg_id: int) -> bool:
    document = db['admins'].find_one({'tg_id': str(tg_id)})

    return document 


async def check_student(tg_id: int) -> bool:
    document = db['students'].find_one({'tg_id': str(tg_id)})

    return document 