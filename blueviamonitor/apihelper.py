import oauth2 as oauth
import time
import httplib
import httplib2


oauth_token = oauth.Token("e0361b2ed52754ae957de9a580be8e3c", "fe590ff6aaab1c3c14bad09e57b44433")
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


# Does not work
def post_sms_json():
    oauth_request = oauth.Request.from_consumer_and_token(
        oauth_consumer, token=oauth_token, http_url=sms_url, parameters={},
    )
    oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), oauth_consumer, oauth_token)

    message = '{"smsText": {"address": {"phoneNumber": "445480605"},"message": "SANDMYKEYWORD This is a fake text message","originAddress": {"alias": "4bf499a1ecaac050dfaddfef87f99e3a"}}}'

    webservice = httplib.HTTPS("api.bluevia.com")
    webservice.putrequest("POST", "/services/REST/SMS_Sandbox/outbound/requests?version=v1")
    webservice.putheader("Host", "api.bluevia.com")
    webservice.putheader("Content-type", "application/json")
    webservice.putheader("Content-length", "%d" % len(message))
    oauth_headers = oauth_request.to_header("https://api.bluevia.com")
    webservice.putheader("Authorization", oauth_headers['Authorization'])
    webservice.endheaders()

    print "Sending " + oauth_headers['Authorization']
    webservice.send(message)

    statuscode, statusmessage, header = webservice.getreply()
    print "Response: ", statuscode, statusmessage, header
