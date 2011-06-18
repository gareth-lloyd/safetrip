from django import forms
from safeweb.models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

