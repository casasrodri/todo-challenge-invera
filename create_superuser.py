import os
import django
from django.contrib.auth import get_user_model
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

User = get_user_model()

username = os.getenv('SUPERUSER_USERNAME')
email = os.getenv('SUPERUSER_EMAIL')
password = os.getenv('SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)