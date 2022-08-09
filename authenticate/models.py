from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_TYPE = [
        ('gestion', 'Gestion'),
        ('vente', 'Vente'),
        ('support', 'Support'),
    ]
    role = models.CharField(choices=ROLE_TYPE,
                            max_length=20)

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.username == "admin" or self.role == "gestion":
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        user = super(User, self)
        user.save()

        return user
