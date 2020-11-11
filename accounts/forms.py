from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone = forms.TextInput(attrs={'required':'True'})
    first_name=forms.TextInput(attrs={'required':'True'})
    last_name=forms.TextInput(attrs={'required':'True'})
    
    class Meta(UserCreationForm.Meta):
        model= CustomUser
        fields = ('first_name','last_name','username','email','phone','password1','password2')
                 

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields