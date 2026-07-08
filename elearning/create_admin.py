import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elearning.settings")

django.setup()

from accounts.models import User

username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superuser créé")
    else:
        print("Superuser existe déjà")
else:
    print("Variables admin manquantes")
