import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

print('--- Last 5 Contacts ---')
for c in db['api_contact'].find().sort('_id', -1).limit(5):
    print(c.get('phone_number'), c.get('name'), c.get('platform_id'))

print('\n--- Last 5 Clients ---')
for c in db['api_client'].find().sort('_id', -1).limit(5):
    print(c.get('business_name'), c.get('whatsapp_phone_number_id'), c.get('whatsapp_waba_id'))

print('\n--- Last 5 Messages ---')
for c in db['api_message'].find().sort('_id', -1).limit(5):
    print(c.get('from_address'), c.get('to_address'), c.get('body'))
