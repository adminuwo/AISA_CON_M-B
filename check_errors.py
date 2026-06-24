import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

print('--- Recent Failed Messages ---')
for msg in db['api_message'].find({"status": "FAILED"}).sort('_id', -1).limit(3):
    print(f"Body: {msg.get('body')}")
    print(f"Metadata (Error Info): {msg.get('metadata')}")
    print("-" * 30)
