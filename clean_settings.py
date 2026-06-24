import sys
content = open('core/settings.py').read()
first_part = content[:content.find('"""\nDjango settings', 10)]
open('core/settings.py', 'w').write(first_part)
