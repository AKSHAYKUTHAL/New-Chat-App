from django.contrib import admin
from .models import CustomUser
from .forms import AdminCustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = AdminCustomUserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['id', 'username', 'email', 'is_registered', 'fname', 'lname']
    list_editable = ['is_registered']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('fname', 'lname', 'email', 'is_registered')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fname', 'lname', 'email', 'is_registered'),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.form = self.add_form
        else:
            self.form = UserChangeForm
        return super().get_form(request, obj, **kwargs)



admin.site.register(CustomUser, CustomUserAdmin)
