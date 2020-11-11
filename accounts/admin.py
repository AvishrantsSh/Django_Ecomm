from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Personal info', {'fields': ('phone','first_name','last_name',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','password1', 'password2'),
        }),
    )
    search_fields = ('username','email')
    ordering = ('username','email')
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)

# Register your models here.
