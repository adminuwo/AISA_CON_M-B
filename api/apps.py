import sys
import os
from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        if 'runserver' in sys.argv:
            from django.db import connections
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                db_name = os.getenv('MONGODB_DB_NAME', 'unknown')
                print(f"\n[OK] SUCCESS: MongoDB connection is ACTIVE! (db: {db_name})\n")
            except Exception as e:
                print(f"\n[ERROR] MongoDB connection FAILED!")
                print(f"Check your .env URL and password. Reason: {str(e)}\n")
