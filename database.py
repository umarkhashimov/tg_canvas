import local_settings as st
from pymongo import MongoClient
from datetime import datetime


client = MongoClient(st.db_connection)
db = client[st.db_name]

async def check_admin(tg_id: int) -> bool:
    document = db['admins'].find_one({'tgid': str(tg_id)})

    return document 

async def get_all_admins():
    data = [x for x in db['admins'].find()]
    return data


async def default_admins():
    for obj in st.DEFAULT_ADMINS:
        data = await check_admin(obj['tgid'])
        if data is None:
            db['admins'].insert_one(obj)

async def check_student(tg_id: int) -> bool:
    document = db['students'].find_one({'tgid': str(tg_id)})

    return document 

async def insert_student(data):
        
    try:
        result = db['students'].insert_one(data)
        return True
    except:
        return False


async def insert_assignment(data):
    try:
        result = db['assignments'].insert_one(data)
        return True
    except:
        return False