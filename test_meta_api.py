import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User

try:
    user = User.objects.get(email='abha@uwo24.com')
    client = user.client
    
    url = f"https://graph.facebook.com/v19.0/{client.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {client.whatsapp_access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": "917694045090",
        "type": "text",
        "text": {"body": "Test message to check token"}
    }
    res = requests.post(url, headers=headers, json=payload)
    print("Meta API Response:", res.status_code, res.text)
except Exception as e:
    print("Error:", e)
