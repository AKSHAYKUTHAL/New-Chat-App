from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    fname = models.CharField(max_length=50, verbose_name="First Name")
    lname = models.CharField(max_length=50, verbose_name="Last Name")
    is_registered = models.BooleanField(default=False, verbose_name="Registered")

    def save(self, *args, **kwargs):
        creating = self._state.adding # checks if the user  is being created
        if creating and (not self.username or not self.password):
            if not self.username:
                random_number = get_random_string(length=2, allowed_chars='0123456789') 
                self.username = f"{self.fname[0]}{self.lname}{random_number}".lower()
            if not self.password:
                self.set_password(get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@-+/*'))
        super().save(*args, **kwargs)
