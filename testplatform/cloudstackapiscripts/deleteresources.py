from django.db import connections, transaction
from testplatform.cloudstackapiscripts.cloudstackapi import CloudstackAPI
from testplatform.cloudstackapiscripts.cloud_test_db import cloud_tests
from dotdictify import dotdictify


@transaction.commit_on_success(using="cloud_tests")
def remove_resource(resource, test_id, api_key, secret_key):


    if resource == 'destroyVirtualMachine':
        sql_query = 'deployvm'
        async_query = 'remove_resourceid.destroyvirtualmachineresponse'

    if resource == 'disassociateIpAddress':
        sql_query = 'associateip'
        async_query = 'remove_resourceid.disassociateipaddressresponse'    

    if resource == 'deleteSnapshot':
        sql_query = 'createsnapshot'
        async_query = 'remove_resourceid.deletesnapshotresponse'

    if resource == 'deleteVolume':
        sql_query = 'createvol'
        async_query = 'remove_resourceid.deletevolumeresponse'

    if resource == 'deleteTemplate':
        sql_query = 'createtemplate'
        async_query = 'remove_resourceid.deletevolumeresponse'

    if resource == 'deleteRemoteAccessVpn':
        sql_query = 'enablevpn'
        async_query = 'remove_resourceid.deleteremoteaccessvpnresponse'


    cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)
    cursor = connections['cloud_tests'].cursor()
    cursor.execute("""select resource_id from %s where resource_id_deleted is null and test_name_id = %%s;""" % (sql_query), (test_id))

    rows = cursor.fetchall()

    for row in rows:

        resource_id = (row[0])
        remove_resourceid = cs_api.request(dict({'command' : resource , 'id' : resource_id }))
        remove_resourceid = dotdictify(remove_resourceid)
        remove_resourceid = async_query

        asnycjob = None

        for key, value in remove_resourceid.items():

            if key == 'jobid' :

                asyncjob = value

                job = CloudstackAPI()
                job.asyncresults(asyncjob,api_key=api_key, secret_key=secret_key)
                remove_resourceid_query = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))

                cursor = connections['cloud_tests'].cursor()
                cursor.execute("""update %s set resource_id_deleted='Y' where test_name_id = %%s and resource_id = %%s""" % (sql_query), (test_id, resource_id))


@transaction.commit_on_success(using="cloud_tests")
def destroyvm(test_id, api_key, secret_key):


    cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)    
    cursor = connections['cloud_tests'].cursor()
    cursor.execute("""select resource_id from deployvm where resource_id_deleted is null and test_name_id = %s;""" % test_id)

    rows = cursor.fetchall()
    
    for row in rows:

        resource_id = (row[0])
        remove_resourceid = cs_api.request(dict({'command':'destroyVirtualMachine' , 'id' : resource_id }))
        remove_resourceid = dotdictify(remove_resourceid)
        remove_resourceid = remove_resourceid.destroyvirtualmachineresponse

        asnycjob = None

        for key, value in remove_resourceid.items():
            
            if key == 'jobid' : 

                asyncjob = value

                job = CloudstackAPI()
                job.asyncresults(asyncjob,api_key=api_key, secret_key=secret_key)
                remove_resourceid_query = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))

                cursor = connections['cloud_tests'].cursor()
                cursor.execute("""update deployvm set resource_id_deleted='Y' where test_name_id = %s and resource_id = %s""" % (test_id, resource_id))


def removeip(test_id, api_key, secret_key):

    cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)
    cursor = connections['cloud_tests'].cursor()
    cursor.execute("""select resource_id from associateip where resource_id_deleted is null and test_name_id = %s;""" % test_id)

    rows = cursor.fetchall()

    for row in rows:

        resource_id = (row[0])
        remove_resourceid = cs_api.request(dict({'command':'disassociateIpAddress' , 'id' : resource_id }))
        remove_resourceid = dotdictify(remove_resourceid)
        remove_resourceid = remove_resourceid.disassociateipaddressresponse

        asnycjob = None

        for key, value in remove_resourceid.items():

            if key == 'jobid' :

                asyncjob = value

                job = CloudstackAPI()
                job.asyncresults(asyncjob,api_key=api_key, secret_key=secret_key)
                remove_resourceid_query = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))


                cursor.execute("""update associateip set resource_id_deleted='Y' where test_name_id = %s and resource_id = %s""" % (test_id, resource_id))


def deletesnapshots(test_id, api_key, secret_key):

    cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)
    cursor = connections['cloud_tests'].cursor()
    cursor.execute("""select resource_id from createsnapshot where resource_id_deleted is null and test_name_id = %s;""" % test_id)

    rows = cursor.fetchall()

    for row in rows:

        resource_id = (row[0])
        remove_resourceid = cs_api.request(dict({'command':'disassociateIpAddress' , 'id' : resource_id }))
        remove_resourceid = dotdictify(remove_resourceid)
        remove_resourceid = remove_resourceid.disassociateipaddressresponse

        asnycjob = None

        for key, value in remove_resourceid.items():

            if key == 'jobid' :

                asyncjob = value

                job = CloudstackAPI()
                job.asyncresults(asyncjob,api_key=api_key, secret_key=secret_key)
                remove_resourceid_query = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))


                cursor.execute("""update createsnapshot set resource_id_deleted='Y' where test_name_id = %s and resource_id = %s""" % (test_id, resource_id))
                transaction.commit_unless_managed()


def deletetemplates(test_id, api_key, secret_key):

    pass
def deletevolumes(test_id, api_key, secret_key):

    pass

def deletepublicips(test_id, api_key, secret_key):

    pass

