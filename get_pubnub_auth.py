import base64
import json
import time
import urllib2


from hashlib import sha512
from hmac import HMAC
from urllib import urlencode

# Add your key and secret
auth_key = ''
auth_secret = ''

url = "https://mtgox.com/api/2/"
path = "stream/private_get"

class request_private:
    def __init__(self, auth_key, auth_secret):
        self.auth_key = auth_key
        self.auth_secret = base64.b64decode(auth_secret)

    def sign_dat(self, secret, data):
        return base64.b64encode(str(HMAC(secret, path+chr(0)+data, sha512).digest()))

    def get_dat_head(self):
        nonce = { "nonce" : int(time.time()*1e6) }
        post_data = urlencode(nonce)
        headers = {
	    'Content-Type' : 'application/x-www-form-urlencoded',
            'User-Agent' : 'MyBot',
            'Rest-Key' : self.auth_key,
            'Rest-Sign' : self.sign_dat(self.auth_secret, post_data)

        }
        return post_data, headers

    def get_priv(self, url):
        post_data, headers = self.get_dat_head()
        request = urllib2.Request(url+path, post_data, headers)
        response = urllib2.urlopen(request, post_data)
        return json.load(response)

r = request_private(auth_key, auth_secret).get_priv(url)
print r

