import oauth2 as oauth
import time
import httplib
import json

POLL_WAIT=30

oauth_token = oauth.Token(key="356810265a6b0a02c85ab718bffa2de1", secret="8cc028d29aa7bfaedc8198a1da0e41df")
oauth_consumer = oauth.Consumer(key='sY11061817851719',secret='GgYe63682680')

sms_url = "https://api.bluevia.com/services/REST/SMS_Sandbox/inbound/445480605/messages?version=v1&alt=json"


def get_sms_json():
    oauth_request = oauth.Request.from_consumer_and_token(
        oauth_consumer, token=oauth_token, http_url=sms_url, parameters={},
    )
    oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), oauth_consumer, oauth_token)

    headers = oauth_request.to_header()
    connection = httplib.HTTPSConnection("api.bluevia.com") # or HTTPSConnection, depending on what you're trying to do
    connection.request("GET", sms_url, headers=headers)

    resp = connection.getresponse()
    return  resp.read()

print get_sms_json()

def get_received_sms():
    return json.loads(get_sms_json())

def start_polling(message_handler):
    print "Sleeping for " + str(POLL_WAIT) + " seconds"
    time.sleep(POLL_WAIT)

    message_handler(get_received_sms())




