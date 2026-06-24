import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User

try:
    user = User.objects.get(email='abha@uwo24.com')
    user.set_password('admin123')
    user.is_active = True  # Ensure the user is active
    user.save()
    print("SUCCESS: Password for abha@uwo24.com has been successfully reset to 'admin123'")
except User.DoesNotExist:
    print("ERROR: User abha@uwo24.com does not exist in Django ORM")
except Exception as e:
    print(f"ERROR: {e}")
