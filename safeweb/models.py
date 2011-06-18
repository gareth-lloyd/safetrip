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
    name = models.CharField(max_length=120)
    secret = models.CharField(max_length=120, unique=True)
    email = models.EmailField(blank=True)

    photo = models.FileField(upload_to='user_photos', blank=True)
    home_contact_email = models.EmailField(blank=True)
    home_contact_mobile = models.CharField(max_length=20, blank=True)

    home_country = CountryField(blank=True)
    home_details = models.CharField(max_length=25, blank=True)
    destination_country = CountryField()
    destination_details = models.CharField(max_length=25, blank=True)

    leaving = models.DateField()
    arriving = models.DateField()

    notes = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUSES, 
        default=0)

    help_country = CountryField(blank=True)
    help_message = models.TextField()
