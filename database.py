import local_settings as st
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os

client = MongoClient(st.db_connection)
db = client[st.db_name]

async def convert_file_name(filename):
    ext = filename.split('.')[-1]
    filename = '{:%Y-%m-%d-%H-%M-%S-%f}.{}'.format(datetime.now(), ext)
    return os.path.join('./submissions/', filename)

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
    
async def is_submitted(assignment_id, user_id):
    query = {
        "$and": [
            {"assignment._id": ObjectId(assignment_id)},
            {"student.tgid": str(user_id)}
        ]
    }
    submission = [x for x in db['submissions'].find(query)]
    return len(submission) > 0

async def select_assignment(userid):
    now = datetime.now()
    query = db['assignments'].find({'due': {'$gt': now}})
    assignments = []

    for obj in query:
        if not await is_submitted(obj['_id'], userid):
            assignments.append(obj)
            
    return assignments

async def get_assignment(id):
    assignment = db['assignments'].find_one({'_id': ObjectId(id)})
    return assignment


async def insert_file_metadata(metadata):
    try:
        result = db['file_metadata'].insert_one(metadata)
        return True
    except:
        return False


async def insert_submission(data):
    try:
        result = db['submissions'].insert_one(data)
        return True
    except:
        return False