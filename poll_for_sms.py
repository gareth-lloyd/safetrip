import sys
from django.core.management import setup_environ
import settings
import blueviamonitor.monitor as monitor

setup_environ(settings)

from safeweb.views import process_secret
from safeweb.models import Traveller, STATUS_SAFE, STATUS_IN_DANGER

country_code = sys.argv[1]
short_code = sys.argv[2]

def update_traveller_for_secret(status, secret, help_country=None, help_message=None):
    processed_secret = process_secret(secret)
    try:
        traveller = Traveller.objects.get(secret=secret)
        traveller.status = status

        if help_country != None:
            traveller_status = help_country

        if help_message != None:
            traveller_status = help_message

        traveller.save()
    except Traveller.DoesNotExist:
        # do stuff
        pass

def handle_sms(sms):
    message_split = sms['message'].split()
    
    if len(message_split) >= 2:
        should_be_HELP_or_pass = message_split[1]
        if should_be_HELP_or_pass.lower() == "help":
            secret = message_split[2]
            update_traveller_for_secret(STATUS_IN_DANGER, secret, help_country)
            print "User with secret " + secret + " is in trouble"
        else:
            secret = message_split[1]
            update_traveller_for_secret(STATUS_SAFE, secret)
            print "User with secret " + secret + " is safe"
    else:
        print "invalid message " + message

monitor.start_polling(short_code, handle_sms)
