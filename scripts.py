import txtlocalsms.send_sms as send_sms

def do_safe_actions(traveller, phone_number=None):
    if phone_number:
        send_sms.send(phone_number, "Glad to hear you're safe.  You can still text SANDSAFETRIP HELP followed by your password if you find yourself in trouble")

def do_help_actions(traveller, phone_number=None):
    if phone_number:
        send_sms.send(phone_number, "Uh oh!")

def do_update_actions(traveller, phone_number=None):
    if phone_number:
        send_sms.send(phone_number, "Thanks. We've forwarded your message.")
