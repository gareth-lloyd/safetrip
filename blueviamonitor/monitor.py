import time
import json
import apihelper

POLL_WAIT=1

def get_received_sms():
    sms_json = apihelper.get_sms_json()

    if len(sms_json) == 0:
        print "No SMS messages found"
        return []
    sms_object = json.loads(sms_json)

    # Shitty json response is an object instead of an array if there's only one
    if type(sms_object['receivedSMS']['receivedSMS']) != list:
        return [sms_object['receivedSMS']['receivedSMS']]
    return sms_object['receivedSMS']['receivedSMS']
    

def start_polling(message_handler):

    while True:
        sms_s = get_received_sms()
        for sms in sms_s:
            message_handler(sms)

        print "Sleeping for " + str(POLL_WAIT) + " seconds"
        time.sleep(POLL_WAIT)





