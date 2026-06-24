from pymongo import MongoClient
from bson.objectid import ObjectId

db = MongoClient('mongodb+srv://admin_db_user:admin%40123@cluster0.drmnlav.mongodb.net/?appName=Cluster0')['aisaconnect_db_v5']
db.api_client.update_one(
    {'_id': ObjectId('6a38f9643a517dd9159ce0c1')},
    {'$set': {'whatsapp_phone_number_id': ''}}
)
print('Updated WOOO client')
