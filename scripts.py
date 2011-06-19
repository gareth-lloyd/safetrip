import txtlocalsms.send_sms as send_sms
import blueviamonitor.apihelper as apihelper
from safeweb.models import HelpDetails

def do_safe_actions(traveller, phone_number=None):
    if phone_number:
        apihelper.post_sms(phone_number, "Glad to hear you're safe.  You can still text SANDSAFETRIP HELP followed by your password if you find yourself in trouble")

def do_help_actions(traveller, phone_number=None, country_code=None):
    if phone_number:

        try:
            country_details = HelpDetails.objects.get(country=country_code)
            apihelper.post_sms(phone_number, country_details.sms_text)
        except HelpDetails.DoesNotExist:
            print "Could not find sms text for " + country_code

def do_update_actions(traveller, phone_number=None):
    if phone_number:
        apihelper.post_sms(phone_number, "Thanks. We've forwarded your message.")

