from django.contrib.auth.models import User
from .models import Profile
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["user_address","user_phone"]