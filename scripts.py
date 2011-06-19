import txtlocalsms.send_sms as send_sms
from safeweb.models import HelpDetails

def do_safe_actions(traveller, phone_number=None):
    if phone_number:
        send_sms.send(phone_number, "Glad to hear you're safe.  You can still text SANDSAFETRIP HELP followed by your password if you find yourself in trouble")

def do_help_actions(traveller, phone_number=None, country_code=None):
    if phone_number:

        try:
            country_details = HelpDetails.objects.get(country=country_code)
            send_sms.send(phone_number, country_details.sms_text)
        except HelpDetails.DoesNotExist:
            print "Could not find sms text for " + country_code

def do_update_actions(traveller, phone_number=None):
    if phone_number:
        send_sms.send(phone_number, "Thanks. We've forwarded your message.")

