from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from safeweb.fields import CountryField

STATUS_IN_TRANSIT = 0
STATUS_IN_DANGER = 1
STATUS_SAFE = 2

STATUSES = (
    (STATUS_IN_TRANSIT, 'In Transit'),
    (STATUS_IN_DANGER, 'In Danger'),
    (STATUS_SAFE, 'Safe'),
)

class Traveller(models.Model):
    created = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=120)
    secret = models.CharField(max_length=120, unique=True)
    email = models.EmailField(blank=True, null=True)

    photo = models.ImageField(upload_to='user_photos', blank=True)
    home_contact_email = models.EmailField(blank=True)
    home_contact_mobile = models.CharField(max_length=20, blank=True)

    home_country = CountryField(blank=True)
    home_details = models.CharField(max_length=25, blank=True)
    destination_country = CountryField()
    destination_details = models.CharField(max_length=25, blank=True)

    arriving = models.DateField()

    notes = models.TextField(null=True, blank=True)

    def _get_current_status(self):
        try:
            return self.travellerupdate_set.order_by('-updated')[0].status
        except IndexError:
            return STATUS_IN_TRANSIT #default

    status = property(_get_current_status)

    def __unicode__(self):
        return self.name

class TravellerUpdate(models.Model):
    updated = models.DateField(auto_now_add=True)
    traveller = models.ForeignKey(Traveller)
    current_country = CountryField()
    update = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)

class HelpDetails(models.Model):
    country = CountryField(primary_key=True)
    web_text = models.TextField()
    sms_text = models.TextField()
