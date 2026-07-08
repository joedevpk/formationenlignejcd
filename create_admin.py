import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ton_projet.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "Joepiako"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="joepiako@gmail.com",
        password="piako2005"
    )
    print("Superuser créé")
else:
    print("Le superuser existe déjà")

