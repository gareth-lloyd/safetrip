import oauth2 as oauth
import time
import httplib
import httplib2
import json

oauth_token = oauth.Token(key="356810265a6b0a02c85ab718bffa2de1", secret="8cc028d29aa7bfaedc8198a1da0e41df")
oauth_consumer = oauth.Consumer(key='sY11061817851719',secret='GgYe63682680')


def get_sms_json(short_code):
    sms_url = "https://api.bluevia.com/services/REST/SMS_Sandbox/inbound/" + short_code + "/messages?version=v1&alt=json"

    oauth_request = oauth.Request.from_consumer_and_token(
        oauth_consumer, token=oauth_token, http_url=sms_url, parameters={},
    )
    oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), oauth_consumer, oauth_token)

    headers = oauth_request.to_header()
    connection = httplib.HTTPSConnection("api.bluevia.com") # or HTTPSConnection, depending on what you're trying to do
    connection.request("GET", sms_url, headers=headers)

    resp = connection.getresponse()
    return  resp.read()


def post_sms(phone_number, text):
    body = {"smsText": {
                "address":          {"phoneNumber":phone_number},
                "message":          text,
                "originAddress":    {"alias": oauth_token.key}, # Sends from this token's mobile number setup in account
                },
            }

    request         = oauth.Request.from_consumer_and_token(oauth_consumer, oauth_token, "POST", "https://api.bluevia.com/services/REST/SMS/outbound/requests?version=v1")
    request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), oauth_consumer, oauth_token)

    body = json.dumps(body)
    connection = httplib.HTTPSConnection("api.bluevia.com")

    headers = request.to_header(realm="https://api.bluevia.com")

    headers.update({'Content-Type': 'application/json'});

    connection.request("POST", "https://api.bluevia.com/services/REST/SMS/outbound/requests?version=v1",headers=headers, body=body)

    resp = connection.getresponse()
    data = resp.read()

    print data, resp.status, resp.reason
