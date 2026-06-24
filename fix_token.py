import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User

try:
    user = User.objects.get(email='abha@uwo24.com')
    client = user.client
    if client:
        # User pasted 'EAGKl...' (lowercase L) but screenshot shows 'EAGKI...' (capital I)
        wrong_token = "EAGKlZCKb8jnEBR6ZC2PkdwQYJ592ecI3AshrXDn6QsackbdNIdsL5IrSi2Td4a35akirT5ZBLHD3Q1GanFS9lFf3doIBECTjf9DlVzYBnlu1qDIp9qOHo2z2bZBbiB0GDf2ZAvvPaCZBa5LK4HZCEwLIg1vZBYLtqXUtnjSXNBAJ3gMVWrXfwV6rRX3sRZAYF6APwDRtpb8G098TywL9ChnYrEzlZB2scGIjasK5o3MSA9LhR3R7VYktVCGP6HD94CntwHZB9y8Kx2hsiLw4ZCIa1U7zcYZBo"
        fixed_token = wrong_token.replace("EAGKl", "EAGKI")
        
        client.whatsapp_access_token = fixed_token
        client.save()
        print(f"SUCCESS: Fixed token spelling mistake and updated!")
except Exception as e:
    print(f"ERROR: {e}")
