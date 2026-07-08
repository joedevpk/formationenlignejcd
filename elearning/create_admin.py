import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elearning.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "Joepiako"
email = "joepiako@gmail.com"
password = "piako2005"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser créé.")
else:
    print("Le superuser existe déjà.")
