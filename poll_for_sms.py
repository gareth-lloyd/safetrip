from django.core.management import setup_environ
import settings
import blueviamonitor.monitor as monitor

setup_environ(settings)

from safeweb.forms import process_secret
from safeweb.models import Traveller, STATUS_SAFE, STATUS_IN_DANGER

def update_traveller_status_for_secret(status, secret):
    processed_secret = process_secret(secret)
    try:
        traveller = Traveller.objects.get(secret=secret)
    except Traveller.DoesNotExist:
        # do stuff
        pass
    traveller.status = status
    traveller.save()

def handle_sms(sms):
    message_split = sms['message'].split()
    
    if len(message_split) >= 2:
        should_be_HELP_or_pass = message_split[1]
        if should_be_HELP_or_pass.lower() == "help":
            secret = message_split[2]
            update_traveller_status_for_secret(STATUS_IN_DANGER, secret)
            print "User with secret " + secret + " is in trouble"
        else:
            secret = message_split[1]
            update_traveller_status_for_secret(STATUS_SAFE, secret)
            print "User with secret " + secret + " is safe"
        
    else:
        print "invalid message " + message

monitor.start_polling(handle_sms)
