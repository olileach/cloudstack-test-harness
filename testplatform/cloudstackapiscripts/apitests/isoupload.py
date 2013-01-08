import urllib
import urllib2
import hmac
import hashlib
import base64
import json
import MySQLdb
import MySQLdb as mdb
import time

class dotdictify(dict):
    marker = object()
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'expected dict'

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, dotdictify):
            value = dotdictify(value)
        dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        found = self.get(key, dotdictify.marker)
        if found is dotdictify.marker:
            found = dotdictify()
            dict.__setitem__(self, key, found)
        return found

    __setattr__ = __setitem__
    __getattr__ = __getitem__



class CloudstackAPI(object):

    def __init__(self, protocol='http', host='10.0.25.14:8080', uri='/client/api', api_key=None, secret_key=None, asyncjob=None, jobresults=None):
        self.protocol = protocol
        self.host = host
        self.uri = uri
        self.api_key = api_key
        self.secret_key = secret_key
        self.errors = []
        self.aysncjob = asyncjob
        self.jobresults = jobresults
    def request(self, params):
        """Builds a query from params and return a json object of the result or None"""
        if self.api_key and self.secret_key:
            # add the default and dynamic params
            params['response'] = 'json'
            params['apiKey'] = self.api_key

            # build the query string
            query_params = map(lambda (k,v):k+"="+urllib.quote(str(v)), params.items())
            query_string = "&".join(query_params)

            # build signature
            query_params.sort()
            signature_string = "&".join(query_params).lower()
            signature = urllib.quote(base64.b64encode(hmac.new(self.secret_key, signature_string, hashlib.sha1).digest()))

            # final query string...
            url = self.protocol+"://"+self.host+self.uri+"?"+query_string+"&signature="+signature

            output = None
            try:
                output = json.loads(urllib2.urlopen(url).read())
            except urllib2.HTTPError, e:
                self.errors.append("HTTPError: "+str(e.code))
            except urllib2.URLError, e:
                self.errors.append("URLError: "+str(e.reason))

            return output
        else:
            self.errors.append("missing api_key and secret_key in the constructor")
            return None

    def asyncresults(self, asyncjob,api_key,secret_key):

        cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)
        qryasyncjob = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        qryasyncjob = dotdictify(qryasyncjob)
        qryasyncjob = qryasyncjob.queryasyncjobresultresponse
        print 'We are waiting for the async API job to complete. Once the job completes, we can action the ouput. '
        print 'Checking jobstatus every 5 secs...'

        for key, value in qryasyncjob.items():
            a = CloudstackAPI()
            if key == 'jobstatus':
                if value == 0:

                    status=0
                    while status==0:

                        qryasyncjob = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
                        qryasyncjob = dotdictify(qryasyncjob)
                        print 'hehehaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaehe', qryasyncjob
                        qryasyncjob = qryasyncjob.queryasyncjobresultresponse

                        for key, value in qryasyncjob.iteritems():
                            if key == 'jobstatus' : status = value
                            if key == 'jobstatus' : print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', value                           
                            if key == 'jobstatus' : a.jobresults = value
                        time.sleep(5)

                    print 'API job complete.'
                    queryasyncjobresponse = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
                    return status

if __name__ == "__main__":


    api_key='YzjA3gIL8rawXZhtuaVCFtAJRIExQG78aPFak7mQ3ZsiSnqNxCF3x38kqryB4GrPYZZw1WIVO9tEWfcwd6bMSQ'
    secret_key='PYIIw--cW5Used-yP2f4b3hQUed700hj6fJADTvXsH2QEAnATuYR2hJk6PN2mMiP2OCHA144ItsTLTdLPqoRbg'
    zone_id = 1 
    cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)
    url = 'http://cdimage.debian.org/debian-cd/6.0.5/i386/iso-cd/debian-6.0.5-i386-businesscard.iso'    


    registerisos = cs_api.request(dict({'command' : 'registerIso', 'osTypeId':'133', 'isfeatured' : '133', 'displayText':'123', 'name':'name123', 'url':url, 'zoneId':zone_id}))
    print registerisos
    registerisos = dotdictify(registerisos)

    print registerisos
    time.sleep (100)

    registerisos = registerisos.listisosresponse.iso
        
