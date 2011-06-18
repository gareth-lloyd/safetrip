from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from safeweb.fields import CountryField

STATUSES = (
    (0, 'In Transit'),
    (1, 'In Danger'),
    (2, 'Safe'),
)
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    photo = models.FileField(upload_to='user_photos')
    home_contact_email = models.EmailField()
    home_contact_mobile = models.CharField(max_length=20)

    home_country = CountryField()
    home_details = models.CharField(max_length=255)
    destination_country = CountryField()
    destination_details = models.CharField(max_length=255)

    leaving = models.DateField()
    arriving = models.DateField()

    notes = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUSES, 
        default=0)
