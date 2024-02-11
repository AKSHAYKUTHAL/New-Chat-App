from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import string
import random

class AdminCustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'fname', 'lname', 'is_registered')

    def __init__(self, *args, **kwargs):
        super(AdminCustomUserCreationForm, self).__init__(*args, **kwargs)
        # Remove username and password requirement for admin form
        if 'username' in self.fields:
            self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

