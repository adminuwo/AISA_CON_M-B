from pymongo import MongoClient
from bson.objectid import ObjectId

db = MongoClient('mongodb+srv://admin_db_user:admin%40123@cluster0.drmnlav.mongodb.net/?appName=Cluster0')['aisaconnect_db_v5']

new_token = "EAGKlZCKb8jnEBR6VPc3tc0hGw005yB1ZBRzSj9Leo2F4alDaw1CgIUqcJvGR5LDGhcSsM7MhyjoB2ftbFrkiAAT0K5k1vPjePowKkSP6yZBY1XWt1KIoTZAmuCF6oZC6ZBiaBfdk658jHaxVF2WveFzkBtSGLgpFScWVC92sW4hJKKgwGYNiKdFCVp37IS2SPhxccMXX7CJmEhW1X0CGUIIhwjfmpD73h06lVKnLynbrgmgEKuocjI6EsyHw7ospr6AmwVvYchBNSAIHcudcl19bNa"

db.api_client.update_one(
    {'_id': ObjectId('6a3a2795f2f0b557ad3db1a6')},
    {'$set': {'whatsapp_access_token': new_token}}
)
print('Token updated successfully!')
