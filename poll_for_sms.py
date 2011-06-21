import sys
from django.core.management import setup_environ
import settings
import blueviamonitor.monitor as monitor

setup_environ(settings)

from safeweb.forms import process_secret
from safeweb.models import Traveller, TravellerUpdate, STATUS_SAFE, STATUS_IN_DANGER, STATUS_IN_TRANSIT
from scripts import do_safe_actions, do_help_actions, do_update_actions

if len(sys.argv) < 3:
    print "Usage eg: python poll_for_sms.py GB 445480605"

country_code = sys.argv[1]
short_code = sys.argv[2]

def update_traveller_for_secret(status, secret, help_country=None, help_message=None, phone_number=None):
    print(secret)
    processed_secret = process_secret(secret)
    try:
        traveller = Traveller.objects.get(secret=processed_secret)
        update = TravellerUpdate(traveller=traveller,
            current_country=help_country, update=help_message,
            status=status)
        update.save()
        if status == STATUS_SAFE:
            do_safe_actions(traveller, phone_number)
        if status == STATUS_IN_DANGER:
            do_help_actions(traveller, phone_number, help_country)
        if status == STATUS_IN_TRANSIT:
            do_update_actions(traveller, phone_number)

    except Traveller.DoesNotExist:
        print "could not find traveller " + processed_secret

def handle_sms(sms):
    message_split = sms['message'].split()
    if len(message_split) >= 2:
        should_be_HELP_UPDATE_or_pass = message_split[1]
        if should_be_HELP_UPDATE_or_pass.lower() == "help":
            secret = message_split[2]

            message = None
            if len(message_split) >= 3:
                message = ' '.join(message_split[3:])

            update_traveller_for_secret(STATUS_IN_DANGER, secret, country_code, message, sms['originAddress']['phoneNumber'])
            print "User with secret " + secret + " is in trouble"
        elif should_be_HELP_UPDATE_or_pass.lower() == "update":
            secret = message_split[2]

            message = None
            if len(message_split) >= 3:
                message = ' '.join(message_split[3:])

            update_traveller_for_secret(STATUS_IN_TRANSIT, secret, country_code, message, sms['originAddress']['phoneNumber'])
            print "User with secret " + secret + " is updating: '" + message + "'"
        else:
            secret = message_split[1]
            update_traveller_for_secret(STATUS_SAFE, secret, None, None, sms['originAddress']['phoneNumber'])
            
            print "User with secret " + secret + " is safe"
    else:
        print "invalid message " + message

monitor.start_polling(short_code, handle_sms)
