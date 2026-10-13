import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.core.management import call_command

django.setup()
call_command('migrate', verbosity=0)

from recipes.services import generate_all

r = generate_all(['chicken', 'tomatoes', 'onion', 'garlic', 'rice'], platform='Instagram', servings=4, difficulty='Easy')
print(r['recipe']['name'])
print(len(r['instructions']))
print(r['local_mode'])
