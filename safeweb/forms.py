from django import forms
from safeweb.models import Traveller

class TravellerForm(forms.ModelForm):
    class Meta:
        model = Traveller
        exclude = ['status']

