import hashlib

from django import forms
from safeweb.models import Traveller
from django.conf import settings

def process_secret(raw_secret):
    secret = raw_secret + settings.SECRET_KEY
    return hashlib.sha256(secret).hexdigest()

MIN_SCRT_LENGTH = 10

class TravellerForm(forms.ModelForm):
    class Meta:
        model = Traveller
        exclude = ['status', 'help_country', 'help_message']

    def clean_secret(self):
        secret = self.cleaned_data['secret']
        if len(secret) < MIN_SCRT_LENGTH:
            raise forms.ValidationError('The secret must be at least 10 characters')
        try:
            Traveller.objects.get(secret=process_secret(secret))
            raise forms.ValidationError('You must choose another secret')
        except Traveller.DoesNotExist:
            pass # the secret is unique: success
        return secret

class SecretFormField(forms.Field):
    def clean(self, value):
        value = super(SecretFormField, self).clean(value)
        if len(value) < MIN_SCRT_LENGTH:
            raise forms.ValidationError('The secret must be at least 10 characters')
        try:
            processed_value = process_secret(value)
            traveller = Traveller.objects.get(secret=processed_value)
        except Traveller.DoesNotExist:
            raise forms.ValidationError('Sorry, that secret is not recognized')
        return processed_value

class HelpForm(forms.Form):
     # country = CountryField
    help_secret = SecretFormField()

class SafeForm(forms.Form):
    safe_secret = SecretFormField()
