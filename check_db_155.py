import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

print('--- Searching for 155 in Contacts ---')
for c in db['api_contact'].find({
    '$or': [
        {'phone_number': {'$regex': '^155'}},
        {'phone_number': {'$regex': '155'}},
        {'platform_id': {'$regex': '^155'}},
        {'platform_id': {'$regex': '155'}}
    ]
}):
    print(c.get('phone_number'), c.get('name'), c.get('platform_id'))

print('\n--- Searching for 155 in Clients ---')
for c in db['api_client'].find({
    '$or': [
        {'whatsapp_phone_number_id': {'$regex': '155'}},
        {'whatsapp_waba_id': {'$regex': '155'}}
    ]
}):
    print(c.get('business_name'), c.get('whatsapp_phone_number_id'), c.get('whatsapp_waba_id'))

print('\n--- Search Complete ---')
