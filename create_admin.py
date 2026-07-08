import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "e-learning.settings"
)

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="Joepiako",
        email="piako@gmail.com",
        password="piako2005"
    )
    print("Superuser créé")
else:
    print("Superuser existe déjà")
