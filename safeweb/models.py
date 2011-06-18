from django.db import models
from django.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)




post_save.connect(page_postsave, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    if create:
        pass

