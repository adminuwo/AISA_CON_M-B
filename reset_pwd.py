import certifi
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

client = MongoClient('mongodb+srv://admin_db_user:admin%40123@cluster0.drmnlav.mongodb.net/?appName=Cluster0', tlsCAFile=certifi.where())
db = client['aisaconnect_db_v5']

hashed_pwd = make_password('admin123')
db.api_user.update_one({'email': 'abha@uwo24.com'}, {'$set': {'password': hashed_pwd}})
print('Password reset successfully to admin123!')
