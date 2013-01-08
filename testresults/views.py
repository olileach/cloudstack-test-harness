from django.db import connections
from django.shortcuts import render_to_response
from django.template import RequestContext
from testresults.sqlrow import SQLRow



def results(request, test_id):

    cursor = connections['cloud_tests'].cursor()

    sql = ("select * from test_criteria where test_id = %s" % (test_id))

    cursor.execute(sql)
    results= [SQLRow(cursor, r) for r in cursor.fetchall()]

    return render_to_response("testresults.html", {'results' : results }, context_instance=RequestContext(request))


