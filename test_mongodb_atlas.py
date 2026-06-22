import os
import sys
from pymongo import MongoClient
from pymongo.errors import OperationFailure, InvalidURI, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the URL from .env
mongo_uri = os.getenv('MONGODB_URI')
db_name = os.getenv('MONGODB_DB_NAME')

print("="*50)
print("🔍 MONGODB ATLAS CONNECTION TEST 🔍")
print("="*50)

if not mongo_uri:
    print("❌ ERROR: MONGODB_URI nahi mili .env file mein!")
    sys.exit(1)

# Hide password for security when printing
masked_uri = mongo_uri
try:
    if "@" in mongo_uri and "://" in mongo_uri:
        parts = mongo_uri.split("@")
        credentials = parts[0].split("://")[1]
        masked_uri = mongo_uri.replace(credentials, "***HIDDEN_CREDENTIALS***")
except:
    pass

print(f"🔗 Testing URL: {masked_uri}")
print(f"📁 Target Database: {db_name}")
print("-" * 50)

try:
    print("⏳ Connecting to MongoDB Atlas... (Please wait)")
    # Connect with a timeout of 5 seconds so it doesn't hang
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Ping the server to check if it's alive
    ping_result = client.admin.command('ping')
    print("✅ SUCCESS: Successfully Connected to MongoDB Atlas!")
    
    # List databases
    databases = client.list_database_names()
    print(f"\n📂 DATABASES FOUND ({len(databases)}):")
    for db in databases:
        print(f"  👉 {db}")
        
    print("-" * 50)
    if db_name in databases:
        print(f"🎉 BINGO! Aapka '{db_name}' database Atlas par ban chuka hai!")
        collections = client[db_name].list_collection_names()
        print(f"📊 Collections inside '{db_name}': {collections}")
    else:
        print(f"⚠️ NOTE: '{db_name}' database abhi tak bana nahi hai. Jaise hi aap frontend se koi data save karenge (ya login karenge), ye automatically ban jayega.")

except InvalidURI as e:
    print("❌ ERROR: Invalid URI!")
    print("   Iska matlab URL ke format mein gadbad hai.")
    print("   HINT: Agar password mein '@' symbol hai, toh usko '%40' likhna zaroori hai.")
    print(f"   Technical Error: {e}")
    
except OperationFailure as e:
    print("❌ ERROR: Authentication Failed!")
    print("   Iska matlab MongoDB Atlas aapka username ya password reject kar raha hai.")
    print("   HINT: Apne Atlas project ke 'Database Access' me jakar password check kijiye.")
    print(f"   Technical Error: {e}")
    
except ServerSelectionTimeoutError as e:
    print("❌ ERROR: Connection Timeout!")
    print("   Iska matlab MongoDB Atlas tak internet pahunch hi nahi pa raha hai.")
    print("   HINT: Atlas ke 'Network Access' me check kijiye ki '0.0.0.0/0' (Allow Access from Anywhere) add hai ya nahi.")
    print(f"   Technical Error: {e}")
    
except Exception as e:
    print(f"❌ UNKNOWN ERROR: {e}")

print("="*50)
