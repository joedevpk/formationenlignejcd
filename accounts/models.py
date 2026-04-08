from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    # rôles
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)
    is_finance_admin = models.BooleanField(default=False)

    #  email unique obligatoire
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        #  sécurité : un formateur ne doit pas être étudiant
        if self.is_instructor:
            self.is_student = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username