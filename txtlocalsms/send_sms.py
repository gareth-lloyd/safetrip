import urllib
import urllib2

def send(to_number, message):

    url = 'https://www.txtlocal.com/sendsmspost.php'
    values = {'uname' : 'tompoges@googlemail.com',
              'pword' : 'solidfail',
              'message' : message,
              'from' : 'Safe Trip',
               'selectednums' : to_number,
                'info' : 1 }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page


