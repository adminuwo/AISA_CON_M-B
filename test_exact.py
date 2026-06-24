import pymongo
import os
import requests
from dotenv import load_dotenv

load_dotenv()
client_mongo = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client_mongo[os.getenv('MONGODB_DB_NAME')]

client_doc = db['api_client'].find_one({"email": "abha@uwo24.com"})
if client_doc:
    token = client_doc.get('whatsapp_access_token')
    phone_id = client_doc.get('whatsapp_phone_number_id')
    
    url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": "917694045090",
        "type": "text",
        "text": {"body": "Testing token directly from DB exact fetch"}
    }
    
    print("Sending to:", url)
    print("Token starts with:", token[:10])
    res = requests.post(url, headers=headers, json=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)
else:
    print("Client not found")
