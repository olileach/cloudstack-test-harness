from django.core.urlresolvers import reverse 
from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from testplatform.forms import TestCriteriaForm
from testplatform.clouddb import Accounts, ServiceOfferings, PublicTemplates, Zones, DiskOfferings
from testplatform.cloudstackapiscripts.cstest import Cloudstack_Tests
import thread
from testplatform.models import CloudStackIpAddress
from django import forms
from testplatform.cloudstackapiscripts.cloud_test_db import cloud_tests
from testresults.sqlrow import SQLRow
from django.db import connections


def testcriteria(request):


    if request.method == 'POST':
        form = TestCriteriaForm(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            
            t_testname = cd['testname']
            t_csmip = cd['csmip'].name
            t_testaccount = cd['testaccount']
            t_listaccount = cd['listaccount']
            t_apikey = cd['apikey']
            t_secretkey = cd['secretkey']
            t_serviceoffering = cd['serviceoffering']
            
            for k, v in ServiceOfferings():
                if v == t_serviceoffering : t_serviceoffering == k             
            
            t_templatename = cd['templatename']

            for k, v in PublicTemplates():
                if v == t_templatename : t_templatename == k

            t_zone = cd['zone']

            for k, v in Zones():
                if v == t_zone : t_zone == k

            t_stopstartvm = cd ['stopstartvm']
            t_rebootvm = cd ['rebootvm']
            t_resetvwpw = cd['resetvwpw']
            t_changesoforvm = cd['changesoforvm']            
            t_changevmso = cd['changevmso']

            #if t_changesoforvm == True:
            #    if t_changevmso == t_serviceoffering:
            #        raise forms.ValidationError("You have selected to change the service offering, but the service offering is the same value as the original service offering. \
            #                                     the service offering to a different value.")
            for k, v in ServiceOfferings():
                if v == t_changevmso : t_changevmso == k

            t_enablestaticnat = cd['enablestaticnat']
            t_fwportfrom = cd['fwportfrom']
            t_fwportto = cd['fwportto']
            t_fwprotocol = cd['fwprotocol']

            t_createipforwarder = cd['createipforwarder']
            t_pfprivateport = cd['pfprivateport']
            t_pfpublicport = cd['pfpublicport']
            t_pfportprotocol = cd['pfportprotocol']
            t_createlb = cd['createlb']
            t_lpprivateport = cd['lpprivateport']
            t_lppublicport = cd['lppublicport']
            t_enablevpn = cd['enablevpn']
            t_addvpnuser = cd['addvpnuser']
            t_snaprootvol = cd['snaprootvol']
            t_createtempfromsnap = cd['createtempfromsnap']
            t_deployvmfromsnap = cd['deployvmfromsnap']
            t_attachdatadatavol = cd['attachdatadatavol']
            t_datavolserviceoffering = cd['datavolserviceoffering']
            
            for k, v in DiskOfferings():
                if v == t_datavolserviceoffering : t_datavolserviceoffering == k

            t_createsnapfromdatavol = cd['createsnapfromdatavol']
            t_createtempfromdatavolsnap = cd['createtempfromdatavolsnap']
            t_createvolfromsnapshot = cd['createvolfromsnapshot']
            t_attachsnapvol = cd['attachsnapvol']
            t_detachdatavol = cd['detachdatavol']
            t_extractdatavol = cd['extractdatavol']
            t_attachiso = cd['attachiso']
            t_rebootvmwiso = cd['rebootvmwiso']
            t_stopstartvmwiso = cd['stopstartvmwiso']
            t_detachiso = cd['detachiso']
            t_uploadiso = cd['uploadiso']
            t_pathtoiso = cd['pathtoiso']
            t_attachuploadediso = cd['attachuploadediso']
            t_detachuploadediso = cd['detachuploadediso']
            t_extractuploadediso = cd['extractuploadediso']
            t_deleteresource = cd['deleteresource']
            submittest = Cloudstack_Tests()

#            These 2 lines are very important. They are used to call asynchronously or synchronously. ASync should be used when fully functional. Sync should be used when in tset mode

            #thread.start_new_thread(submittest.intialise_test,
            #submittest.intialise_test

            sqlupdate = cloud_tests()
            test_id = sqlupdate.tbl_test_name(t_testname)
        

            sqlupdate.tbl_test_criteria(test_id, t_testname, t_listaccount, t_templatename, t_zone, t_stopstartvm, t_rebootvm, t_resetvwpw, t_changesoforvm,
                                        t_enablestaticnat, t_createipforwarder, t_createlb, t_enablevpn, t_snaprootvol, t_createtempfromsnap ,t_deployvmfromsnap,
                                        t_attachdatadatavol, t_createsnapfromdatavol, t_createtempfromdatavolsnap, t_createvolfromsnapshot, t_attachsnapvol,
                                        t_detachdatavol, t_extractdatavol, t_attachiso, t_rebootvmwiso, t_stopstartvmwiso, t_detachiso, t_uploadiso, 
                                        t_attachuploadediso, t_detachuploadediso, t_extractuploadediso)

            thread.start_new_thread(submittest.intialise_test,(t_csmip, t_testaccount, t_listaccount, t_apikey, t_secretkey, t_serviceoffering, t_templatename, 
                                      t_zone, t_resetvwpw, t_changesoforvm, t_changevmso, t_stopstartvm, t_rebootvm, t_enablevpn, t_addvpnuser,
                                      t_enablestaticnat, t_fwportfrom, t_fwportto, t_fwprotocol, t_createipforwarder, t_pfprivateport, t_pfpublicport,
                                      t_pfportprotocol, t_createlb, t_lpprivateport, t_lppublicport, t_snaprootvol, t_createtempfromsnap, t_deployvmfromsnap,
                                      t_attachdatadatavol, t_datavolserviceoffering, t_createsnapfromdatavol, t_createtempfromdatavolsnap, 
                                      t_createvolfromsnapshot, t_attachsnapvol, t_detachdatavol,
                                      t_extractdatavol, t_attachiso, t_rebootvmwiso, t_stopstartvmwiso, t_detachiso, t_uploadiso, t_pathtoiso, t_attachuploadediso,
                                      t_detachuploadediso, t_extractuploadediso, t_deleteresource))

            return HttpResponseRedirect(reverse('testresults.views.results', args=(test_id,)))            
                
    else:
        form = TestCriteriaForm()
    c = { 'form' : form }
    return render(request, 'submit.html', c)

