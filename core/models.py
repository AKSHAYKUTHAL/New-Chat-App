from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from core.utils import send_user_registration_email

class CustomUser(AbstractUser):
    fname = models.CharField(max_length=50, verbose_name="First Name")
    lname = models.CharField(max_length=50, verbose_name="Last Name")
    is_registered = models.BooleanField(default=False, verbose_name="Registered")

    def save(self, *args, **kwargs):
        creating = self._state.adding
        if creating:
            random_number = get_random_string(length=2, allowed_chars='0123456789') 
            self.username = f"{self.fname[0]}{self.lname}{random_number}".lower()
        
            temp_password = get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@-+/*')
            self.set_password(temp_password)
        super().save(*args, **kwargs)


        if creating and not self.is_registered :
            mail_template = 'core/user_registered_email.html'
            context = {
                'user' : self,
                'is_registered' : self.is_registered,
                'temp_password':temp_password,
                'temp_username':self.username
            }
            mail_subject = 'Congatulation. Your account has been registered succesfully'
            send_user_registration_email(mail_subject, mail_template, context)


            

