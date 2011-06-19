from django.contrib import admin

from safeweb.models import *

class TravellerUpdateAdmin(admin.ModelAdmin):
    list_display = ('traveller', 'updated',)
    pass

class TravellerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    pass

class HelpDetailsAdmin(admin.ModelAdmin):
    list_display = ('country',)
    pass

admin.site.register(Traveller, TravellerAdmin)
admin.site.register(TravellerUpdate, TravellerUpdateAdmin)
admin.site.register(HelpDetails, HelpDetailsAdmin)


