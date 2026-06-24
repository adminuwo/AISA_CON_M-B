import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

search_term = '155'
print(f'--- Searching for {search_term} everywhere ---')

for coll_name in db.list_collection_names():
    results = list(db[coll_name].find())
    found = []
    for doc in results:
        # Check all string values in doc
        for key, value in doc.items():
            if isinstance(value, str) and search_term in value:
                found.append(f"Field: {key}, Value: {value}")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and search_term in item:
                        found.append(f"Field: {key}, Value (in list): {item}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, str) and search_term in v:
                        found.append(f"Field: {key}.{k}, Value: {v}")
    
    if found:
        print(f"\nCollection: {coll_name}")
        for f in found:
            print(f"  - {f}")

print('\n--- Search Complete ---')
