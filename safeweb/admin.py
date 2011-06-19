from django.contrib import admin

from safeweb.models import *

class TravellerUpdateAdmin(admin.ModelAdmin):
    list_display = ('traveller', 'updated', 'current_country')

class TravellerAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HelpDetailsAdmin(admin.ModelAdmin):
    list_display = ('country',)

admin.site.register(Traveller, TravellerAdmin)
admin.site.register(TravellerUpdate, TravellerUpdateAdmin)
admin.site.register(HelpDetails, HelpDetailsAdmin)


