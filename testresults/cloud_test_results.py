from django.db import connections
from django.shortcuts import render_to_response
from django.template import RequestContext


class testresults:

    #test_name = []
    #accounts = []

    def accounts(self):

        accounts = []

        cursor = connections['cloud_tests'].cursor()
        cursor.execute('SELECT * FROM accounts')
        res = cursor.fetchall()

        for v in res[::]:
            accounts.append(v)

        testresults.accounts = accounts 

    def test_name(self):

        test_name = []

        cursor = connections['cloud_tests'].cursor()
        cursor.execute('SELECT * FROM test_name')
        res = cursor.fetchall()
 
        for v in res[::]:
            test_name.append(v)

        testresults.test_name = test_name

