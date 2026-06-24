import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

print('--- Users ---')
for u in db['api_user'].find({}, {'username': 1, 'email': 1, 'role': 1}):
    print(u)
