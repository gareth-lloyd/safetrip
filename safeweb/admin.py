from django.contrib import admin

from safeweb.models import Traveller

class TravellerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Traveller, TravellerAdmin)
