import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User

try:
    user = User.objects.get(email='abha@uwo24.com')
    client = user.client
    if client:
        client.whatsapp_access_token = "EAGKlZCKb8jnEBR1HPKH6Lgwk11CrquaIYqicCuJ7CCGOu7MhLZCyVXAZC671YcNZBLr3xc1Io1kmWaK4vnUqdxAhZCfgSZADEHHgMg6rf5lIVWqfrA5YXfY7MwE6KPHpyowv1MMM9FtJPNvHeBwPmte4z1zxMJUeGUTCsSboMxkHGHH3x93553TIZBGBRdldWGAb0STHpUJnKylRVnbTo2ZApppHI2hFmbQZBBWcBX5YIe2QT9wi2LsP4yhgm2iDl5B23Fd0eaAsACviudveZCzd5w5ucu"
        client.save()
        print("SUCCESS: Updated with exact access token")
except Exception as e:
    print(f"ERROR: {e}")
