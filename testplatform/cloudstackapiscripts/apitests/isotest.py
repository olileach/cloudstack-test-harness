import urllib2
import urllib
import json
import hmac
import base64
import hashlib
import re

class BaseClient(object):
    def __init__(self, api, apikey, secret):
        self.api = api
        self.apikey = apikey
        self.secret = secret

    def request(self, command, args):
        args['apikey'] = self.apikey
        args['command'] = command
        args['response'] = 'json'
        
        params=[]
        
        keys = sorted(args.keys())

        for k in keys:
            params.append(k + '=' + urllib.quote_plus(args[k]))
       
        query = '&'.join(params)

        signature = base64.b64encode(hmac.new(
            self.secret,
            msg=query.lower(),
            digestmod=hashlib.sha1
        ).digest())

        query += '&signature=' + urllib.quote_plus(signature)

        response = urllib2.urlopen(self.api + '?' + query)
        decoded = json.loads(response.read())
       
        propertyResponse = command.lower() + 'response'
        if not propertyResponse in decoded:
            if 'errorresponse' in decoded:
                raise RuntimeError("ERROR: " + decoded['errorresponse']['errortext'])
            else:
                raise RuntimeError("ERROR: Unable to parse the response")

        response = decoded[propertyResponse]
        result = re.compile(r"^list(\w+)s").match(command.lower())

        if not result is None:
            type = result.group(1)

            if type in response:
                return response[type]
            else:
                # sometimes, the 's' is kept, as in :
                # { "listasyncjobsresponse" : { "asyncjobs" : [ ... ] } }
                type += 's'
                if type in response:
                    return response[type]

        return response


if __name__ == "__main__":


    apikey='YzjA3gIL8rawXZhtuaVCFtAJRIExQG78aPFak7mQ3ZsiSnqNxCF3x38kqryB4GrPYZZw1WIVO9tEWfcwd6bMSQ'
    secretkey='PYIIw--cW5Used-yP2f4b3hQUed700hj6fJADTvXsH2QEAnATuYR2hJk6PN2mMiP2OCHA144ItsTLTdLPqoRbg'
    cs_api = BaseClient(api,apikey=apikey, secret=secretkey)

    url = 'www.mirrorservice.org/pub/OpenBSD/5.1/i386/cd51.iso'
    api={'zoneid':'1','name':'asas','command':'registerIso','url':'isourl','osTypeId':'133','displayText':'myyiso'}
    cs_api.request(dict({'zoneid':'1','name':'asas','command':'registerIso','url':'isourl','osTypeId':'133','displayText':'myyiso'}))
    b = cs_api.request(dict({'command':'listisos'}))
