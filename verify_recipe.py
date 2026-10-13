import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from recipes.services import generate_all
r = generate_all(['chicken', 'tomatoes', 'onion', 'garlic', 'rice'], platform='Instagram', servings=4, difficulty='Easy')
print(r['recipe']['name'])
print(len(r['instructions']))
print(r['local_mode'])
