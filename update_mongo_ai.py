import certifi
from pymongo import MongoClient

uri = 'mongodb+srv://admin_db_user:admin%40123@cluster0.drmnlav.mongodb.net/?appName=Cluster0'
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['aisaconnect_db_v5']

db.api_client.update_many({}, {
    '$set': {
        'ai_enabled': True
    }
})
print('Updated all clients to have AI Enabled!')
