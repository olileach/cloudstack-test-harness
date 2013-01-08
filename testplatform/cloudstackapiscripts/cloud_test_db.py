import MySQLdb
import MySQLdb as mdb
from testplatform.models import DbConfig
#from testplatform.cloudstackapiscripts.cstest import Cloudstack_Tests


class cloud_tests():

    # Get DbConfig vlass values from testplatform.models. Entries are inputted in by admin site and are to set the cloud_tests DB settings.

    sql_host, sql_user, sql_password, sql_database = None, None, None, None
    values = DbConfig.objects.filter(db_purpose='cloud_tests').values()
    
    for v in values:
        dict_values = v
    
    for k, v in dict_values.iteritems():
        if k == 'sql_host' : sql_host = v
        if k == 'sql_user' : sql_user = v
        if k == 'sql_password' :  sql_password = v
        if k == 'sql_database' :  sql_database = v

    testname = None

    sql_conn = mdb.connect('localhost', 'pydba', 'python', 'cloud_tests');
    tbl_accountid = None
    tbl_test_nameid = None

    def __init__(self, vmid=None, account_id=None, account_name=None, domain_id=None, domain=None, username=None, first_name=None, last_name=None, email=None, \
                 testname=testname, cmd=None, name=None, displayname=None, state=None, cpunumber=None, cpuspeed=None, memory=None, guestosid=None,  \
                 templatename=None, hypervisor=None, serviceofferingid=None, serviceofferingname=None, created=None, async_jobid=None, jobstatus=None, \
                 resource_id=None, ipaddress=None, gateway=None, networkid=None, iprole=None, ipid=None, natstatus=None, publicipaddress=None, \
                 pubstartport = None, pubendport = None, privstartport = None, privendport = None, protocol = None , vmname = None, privateport = None, \
                 publicport = None , lbvmid = None, storage = None, attached = None, diskofferingid = None, vmstate = None, diskname = None, extractable = None, \
                 disktype = None, size = None, templatetype = None, file_type = None, isfeatured = None , sourcetemplateid = None, \
                 snapshotname = None, volumename = None, volumeid = None, snapshottype = None, isoid = None, isoname = None, attachediso = None, reboottime = None, \
                 isodetached = None, detachedtime = None, disksize = None, timezone = None, maxsnaps = None, schedule = None, intervaltype = None, stoptime = None, \
                 starttime = None):

        self.vmid = vmid
        self.account_id = account_id
        self.account_name = account_name
        self.domain_id = domain_id
        self.domain = domain
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.testname = testname
        self.cmd = cmd
        self.name = name
        self.displayname= displayname
        self.state = state
        self.cpunumber = cpunumber
        self.cpuspeed = cpuspeed
        self.memory = memory
        self.guestosid = guestosid
        self.templatename = templatename
        self.hypervisor = hypervisor
        self.serviceoffingid = serviceofferingid
        self.serviceofferingname = serviceofferingname
        self.created= created
        self.async_jobid = async_jobid
        self.jobstatus = jobstatus
        self.resource_id = resource_id
        self.ipaddress = ipaddress
        self.gateway = gateway
        self.networkid = networkid
        self.ipid = ipid
        self.publicipaddress = publicipaddress
        self.iprole = iprole
        self.natstatus = natstatus
        self.pubstartport = pubstartport
        self.pubendport = pubendport
        self.privstartport = privstartport
        self.privendport = privendport
        self.state = state
        self.protocol = protocol
        self.vmname = vmname
        self.privateport = privateport
        self.publicport = publicport
        self.lbvmid = lbvmid
        self.storage = storage
        self.attached = attached
        self.difskofferingid = diskofferingid
        self.vmstate = vmstate
        self.diskname = diskname
        self.extractable = extractable
        self.disktype = disktype
        self.size = size
        self.templatetype = templatetype
        self.file_type = file_type
        self.isfeatured = isfeatured
        self.sourcetemplateid = sourcetemplateid
        self.isoid = isoid
        self.isoname = isoname
        self.attachediso = attachediso
        self.reboottime = reboottime
        self.isodetached = isodetached
        self.detachedtime = detachedtime
        self.disksize = disksize
        self.timezone = timezone
        self.maxsnaps = maxsnaps
        self.schedule = schedule
        self.intervaltype = intervaltype
        self.stoptime = stoptime
        self.starttime = starttime


    def tbl_test_criteria_status(self, r_testname, t_testname, jobresult, testid):
       
        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("""UPDATE test_criteria SET %s=%%s WHERE test_id=%%s""" % r_testname, (jobresult, testid))
        con.commit()

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("""UPDATE test_criteria SET %s='2' WHERE test_id=%%s""" % t_testname, (testid))
        con.commit()


    def tbl_test_criteria(self, test_id, t_testname, t_listaccount, t_templatename, t_zone, t_stopstartvm, t_rebootvm, t_resetvwpw, t_changesoforvm,
                          t_enablestaticnat, t_createipforwarder, t_createlb, t_enablevpn, t_snaprootvol, t_createtempfromsnap ,t_deployvmfromsnap,
                          t_attachdatadatavol, t_createsnapfromdatavol, t_createtempfromdatavolsnap, t_createvolfromsnapshot, t_attachsnapvol,
                          t_detachdatavol, t_extractdatavol, t_attachiso, t_rebootvmwiso, t_stopstartvmwiso, t_detachiso, t_uploadiso,
                          t_attachuploadediso, t_detachuploadediso, t_extractuploadediso):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO test_criteria(test_id, t_testname, t_listaccount, t_templatename, t_zone, t_stopstartvm, t_rebootvm, t_resetvwpw, t_changesoforvm,\
                        t_enablestaticnat, t_createipforwarder, t_createlb, t_enablevpn, t_snaprootvol, t_createtempfromsnap ,t_deployvmfromsnap,\
                        t_createdatavol, t_attachdatadatavol, t_createsnapfromdatavol, t_createtempfromdatavolsnap, t_createvolfromsnapshot, t_attachsnapvol,\
                        t_detachdatavol, t_extractdatavol, t_attachiso, t_rebootvmwiso, t_stopstartvmwiso, t_detachiso, t_uploadiso,\
                        t_attachuploadediso, t_detachuploadediso, t_extractuploadediso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",\
                        (test_id, t_testname, t_listaccount, t_templatename, t_zone, t_stopstartvm, t_rebootvm, t_resetvwpw, t_changesoforvm,\
                        t_enablestaticnat, t_createipforwarder, t_createlb, t_enablevpn, t_snaprootvol, t_createtempfromsnap ,t_deployvmfromsnap,\
                        t_attachdatadatavol, t_attachdatadatavol, t_createsnapfromdatavol, t_createtempfromdatavolsnap, t_createvolfromsnapshot, t_attachsnapvol,\
                        t_detachdatavol, t_extractdatavol, t_attachiso, t_rebootvmwiso, t_stopstartvmwiso, t_detachiso, t_uploadiso,\
                        t_attachuploadediso, t_detachuploadediso, t_extractuploadediso))
        con.commit()
        
        
    def tbl_test_name(self, t_testname):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO test_name(test_name) VALUES(%s)",(t_testname))
        con.commit()

        cursor.execute("SELECT max(id) FROM `cloud_tests`.`test_name`")
        con.commit()
        tbl_test_nameid_rs = cursor.fetchone()
        cloud_tests.tbl_test_nameid = tbl_test_nameid_rs[0]

        return tbl_test_nameid_rs[0]

    def tbl_accounts(self, account_id, account_name, domain_id, domain_name, username, first_name, last_name, email):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO accounts(account_id, account_name, domain_id, domain,\
                        username, first_name, last_name, email) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", \
                       (account_id, account_name, domain_id, domain_name, username, first_name, last_name, email))
        con.commit()

        cursor.execute("SELECT max(id) FROM `cloud_tests`.`accounts`")
        tbl_accountid_rs = cursor.fetchone()
        cloud_tests.tbl_accountid = tbl_accountid_rs[0]
        
        con.commit()

    def tbl_deployvm(self, vmid, name, displayname, state, cpunumber, cpuspeed, memory, guestosid, templatename, hypervisor,\
                     serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, created, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO deployvm(vmid, name, displayname, state, cpunumber, cpuspeed, memory, guestosid, templatename, hypervisor,\
                        serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, created, resource_id, accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (vmid, name, displayname, state, cpunumber, cpuspeed, memory, guestosid, templatename, hypervisor, \
                        serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, created, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_changevmso(self, vmid, newso, oldso):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO changevmso(vmid, newso, oldso, accounts_id, test_name_id) VALUES(%s,%s,%s,%s,%s)", \
                    (vmid, newso, oldso, cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_resetvmpw(self, vmid, vmname, displayname, templatename, serviceofferingid, password, passwordenabled, asyncjob):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO resetvmpw(vmid, vmname, displayname, templatename, serviceofferingid, password, passwordenabled, async_jobid, accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (vmid, vmname, displayname, templatename, serviceofferingid, password, passwordenabled, asyncjob, cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()
    
    def tbl_associateip(self, ipid, publicipaddress, iprole, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO associateip(ipid, publicipaddress, iprole, resource_id, accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s)", \
                        (ipid, publicipaddress, iprole, resource_id, cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_staticnat(self, ipid, vmid, natstatus, publicendport, privateendport, protocol, state,resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO staticnat(ipid, vmid, natstatus, startport, endport, protocol, state, resource_id, accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (ipid, vmid, natstatus, publicendport, privateendport, protocol, state,  resource_id, cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_portfwrule(self, ipid , pubstartport, pubendport, privstartport, privendport, state, protocol, vmname, vmid, resource_id, jobstatus):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO portfwrule(ipid , pubstartport, pubendport, privstartport, privendport, state, protocol, vmname, vmid, \
                        resource_id, jobstatus, accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (ipid , pubstartport, pubendport, privstartport, privendport, state, protocol, vmname, vmid, resource_id, jobstatus, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_lbrule(self, algorithm, ipid, publicipaddress, privateport, publicport, lbvmid, resource_id, jobstatus):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO lbrule( algorithm, ipid, publicipaddress, privport, pubport, lbvmid, resource_id, \
                        jobstatus, accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (algorithm, ipid, publicipaddress, privateport, publicport, lbvmid, resource_id, jobstatus, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_enablevpn(self, publicip, pub_ipid, iprange, presharedkey, account, state, addvpnuser, vpnuser, asyncjob, resource_id ):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO enablevpn( publicipaddress, ipid, iprange, presharedkey, account, state, addvpnuser, vpnuser, async_jobid, resource_id, \
                    accounts_id, test_name_id) \
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                    (publicip, pub_ipid, iprange, presharedkey, account, state, vpnuser, addvpnuser, asyncjob, resource_id, \
                    cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_createsnapshot(self, snapshotname, volumename, created, volumeid, snapshottype, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO createsnapshot( snapshotname, volumename, created, volumeid, snapshottype, resource_id , \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (snapshotname, volumename, created, volumeid, snapshottype, resource_id , \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_createtemplate(self, displayname, templatetype, status, file_type, isfeatured, sourcetemplateid, templatename, hypervisor, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO createtemplate( displayname, templatetype, status, file_type, isfeatured, sourcetemplateid, templatename, hypervisor, resource_id, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (displayname, templatetype, status, file_type, isfeatured, sourcetemplateid, templatename, hypervisor, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_createvol(self, diskname, extractable, state, disktype, size, diskofferingid, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO createvol( diskname, extractable, state, disktype, size, diskofferingid, resource_id, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (diskname, extractable, state, disktype, size, diskofferingid, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_attachvol(self, vmname, storage, state, vmid, created, attached, diskofferingid, vmstate, hypervisor, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO attachvol( vmname, storage, state, vmid, created, attached, diskofferingid, vmstate, hypervisor, resource_id, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (vmname, storage, state, vmid, created, attached, diskofferingid, vmstate, hypervisor, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_detachvol(self, diskname, detached, detachedtime, disktype, storage, hypervisor, disksize, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO detachvol( diskname, detached, detachedtime, disktype, storage, hypervisor, disksize, resource_id, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (diskname, detached, detachedtime, disktype, storage, hypervisor, disksize, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_downloadvol(self, extractmode, dwnlstate, url, volnamedownloaded, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO downloadvol(extractmode, dwnlstate, url, volnamedownloaded, resource_id, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s)", \
                        (extractmode, dwnlstate, url, volnamedownloaded, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()


    def tbl_stopvm(self, stoptime, vmname, hypervisor, resource_id, attachediso, isoid, isoname):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO stopvm( stoptime, vmname, hypervisor, resource_id, attachediso, isoid, isoname, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (stoptime, vmname, hypervisor, resource_id, attachediso, isoid, isoname, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_startvm(self, starttime, vmname, hypervisor, resource_id, attachediso, isoid, isoname):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO startvm( starttime, vmname, hypervisor, resource_id, attachediso, isoid, isoname, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                        (starttime, vmname, hypervisor, resource_id, attachediso, isoid, isoname, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_rebootvm(self, vmname, vmid, attachediso, reboottime):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO rebootvm( vmname, vmid, attachediso, reboottime, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s)", \
                        (vmname, vmid, attachediso, reboottime, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_attachiso(self, isoid, isoname, vmname, vmid, resource_id):

        con = cloud_tests.sql_conn
        cursor = con.cursor()
        cursor.execute("INSERT INTO attachiso( isoid, isoname, vmname, vmid, resource_id, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s)", \
                        (isoid, isoname, vmname, vmid, resource_id, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()

    def tbl_detachiso(self, isodetached, vmname, vmid, detachedtime):

        con = cloud_tests.sql_conn        
        cursor = con.cursor()
        cursor.execute("INSERT INTO detachiso( isodetached, vmname, vmid, detachedtime, \
                        accounts_id, test_name_id) \
                        VALUES(%s,%s,%s,%s,%s,%s)", \
                        (isodetached, vmname, vmid, detachedtime, \
                        cloud_tests.tbl_accountid, cloud_tests.tbl_test_nameid))
        con.commit()
