import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

print('--- Recent Messages (Last 5) ---')
for msg in db['api_message'].find().sort('_id', -1).limit(5):
    print(f"[{msg.get('message_type')}] Status: {msg.get('status')} | From: {msg.get('from_address')} | To: {msg.get('to_address')} | Body: {msg.get('body')}")
