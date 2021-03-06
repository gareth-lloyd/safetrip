import hashlib

from django import forms
from safeweb.models import Traveller
from safeweb.fields import COUNTRIES
from django.conf import settings

def process_secret(raw_secret):
    secret = raw_secret.lower() + settings.SECRET_KEY
    return hashlib.sha256(secret).hexdigest()

MIN_SCRT_LENGTH = 10
SECRET_LABEL = "Your secret code"
SECRET_HELP = "Tell us the secret you got when you signed up"

class TravellerForm(forms.ModelForm):
    class Meta:
        model = Traveller
        widgets = {'destination_details': forms.Textarea, 
                   'home_details': forms.Textarea}
        exclude = ['secret', 'status', 'help_country', 'help_message']

class CountryField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', COUNTRIES)
        kwargs.setdefault('help_text', 'Tell us where you are')
        super(CountryField, self).__init__(*args, **kwargs)

class SecretFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', SECRET_LABEL)
        kwargs.setdefault('help_text', SECRET_HELP)
        super(SecretFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None or len(value) < MIN_SCRT_LENGTH:
            raise forms.ValidationError('The secret must be at least 10 characters')
        return process_secret(value.lower())

def _clean_secret(form_instance, name):
    data = form_instance.cleaned_data
    try:
        traveller = Traveller.objects.get(secret=data[name])
        data['traveller'] = traveller
    except Traveller.DoesNotExist:
        raise forms.ValidationError('Sorry, that secret word is not recognized')
    return data

class HelpForm(forms.Form):
    country = CountryField(required=False)
    help_message = forms.CharField(help_text='Tell us how you are', required=False, widget=forms.Textarea)
    help_secret = SecretFormField(required=False)

    def clean_help_secret(self):
        return _clean_secret(self, 'help_secret')

class UpdateForm(forms.Form):
    country = CountryField(label="Where are you?", required=False)
    message = forms.CharField(help_text="Tell us what's happening", 
                              required=False, widget=forms.Textarea)
    update_secret = SecretFormField(required=False)

    def clean_update_secret(self):
        return _clean_secret(self, 'update_secret')

class SafeForm(forms.Form):
    safe_secret = SecretFormField(required=False)

    def clean_safe_secret(self):
        return _clean_secret(self, 'safe_secret')

