import dotdictify
import cloud_test_db
import thread
import MySQLdb
import MySQLdb as mdb
import time

from dotdictify import dotdictify
from testplatform.cloudstackapiscripts.cloud_test_db import cloud_tests
from testplatform.cloudstackapiscripts.cloudstackapi import CloudstackAPI
from testplatform.models import DbConfig
from testplatform.cloudstackapiscripts import deleteresources


class Cloudstack_Tests():

    # Setting class variables that are common between functions so they can be set and called whenever required
        
    sqlupdate = cloud_test_db.cloud_tests() # used by functionfor mysql inserts

    api_key = None
    secret_key = None
    csmip = None
    vmid = None # set by def deployvm
    so_id = None # set by intialise_test
    template_id = None # set by intialise_test
    zone_id = None # set by intialise_test
    ostypeid = None # set by def deployvm
    iprole = None # set by assign_ip 
    pub_ipid = None # set by assign_ip
    lbid = None
    datavol_id = None
    snap_id = None # set by snapshot_root
    snaptemplate_id = None # root_snap_template
    createtemp_vmid = None
    vmso = None
    sourcenat_id = None
    addvpnuser = None

    def __init__(self, api_key=None, secret_key=None):
        
        self.api_key = api_key
        self.secret_key = secret_key

    def testaccount_random(self):

        # This queries the cloud DB and returns api and secret keys for valid enabled account. 
        # It uses the RAND() function to randomly pick an account. Only one account is returns by limit 1

        sql_host, sql_user, sql_password, sql_database = None, None, None, None
        values = DbConfig.objects.filter(db_purpose='cloudstack').values()

        for v in values:
            dict_values = v

        for k, v in dict_values.iteritems():
            if k == 'sql_host' : sql_host = v
            if k == 'sql_user' : sql_user = v
            if k == 'sql_password' :  sql_password = v
            if k == 'sql_database' :  sql_database = v

        # SQL query to get randoom account in cloudstack. Account must be enabled

        con = mdb.connect(sql_host, sql_user, sql_password, sql_database);
        cursor = con.cursor()
        cursor.execute ("""select cu.api_key, cu.secret_key, ca.account_name, cd.name, cu.username,  \
                         ca.id, cd.id, cu.firstname, cu.lastname, cu.email \
                         from cloud.account ca \
                         join cloud.user cu on cu.account_id = ca.id \
                         join cloud.domain cd on cd.id = ca.domain_id \
                         where ca.state = 'enabled' and cu.api_key is not null and cu.secret_key is not null \
                         order by RAND() limit 1;""")

        #con.commit()

        rows = cursor.fetchall()

        api_key_rs, secret_key_rs, account_name, domain_name, username, account_id, domain_id, first_name, last_name, email  \
        = None, None, None, None, None, None, None, None, None, None

        for row in rows:

            api_key_rs = (row[0])
            secret_key_rs = (row[1])
            account_name = (row[2])
            domain_name = (row[3])
            username = (row[4])
            account_id = (row[5])
            domain_id = (row[6])
            first_name = (row[7])
            last_name = (row[8])
            email = (row[9])
        
        con.commit()

        Cloudstack_Tests.api_key = api_key_rs
        Cloudstack_Tests.secret_key = secret_key_rs

        # Inserting test accounts details in to tbl_accounts

        Cloudstack_Tests.sqlupdate.tbl_accounts(account_id, account_name, domain_id, domain_name, username, first_name, last_name, email)

    def testaccount_list(self, t_testaccount):

        # This queries the cloud DB and returns api and secret keys for valid enabled account.
        # It uses the RAND() function to randomly pick an account. Only one account is returns by limit 1

        sql_host, sql_user, sql_password, sql_database = None, None, None, None
        values = DbConfig.objects.filter(db_purpose='cloudstack').values()

        for v in values:
            dict_values = v

        for k, v in dict_values.iteritems():
            if k == 'sql_host' : sql_host = v
            if k == 'sql_user' : sql_user = v
            if k == 'sql_password' :  sql_password = v
            if k == 'sql_database' :  sql_database = v

        con = mdb.connect(sql_host, sql_user, sql_password, sql_database);
        cursor = con.cursor()
        cursor.execute ("""select cu.api_key, cu.secret_key, ca.account_name, cd.name, cu.username, \
                            ca.id, cd.id, cu.firstname, cu.lastname, cu.email \
                            from cloud.account ca \
                            join cloud.user cu on cu.account_id = ca.id \
                            join cloud.domain cd on cd.id = ca.domain_id \
                            where ca.account_name = %s;""", (t_testaccount))

        con.commit()

        rows = cursor.fetchall()

        api_key_rs, secret_key_rs, account_name, domain_name, username, account_id, domain_id, first_name, last_name, email  \
        = None, None, None, None, None, None, None, None, None, None

        for row in rows:

            api_key_rs = (row[0])
            secret_key_rs = (row[1])
            account_name = (row[2])
            domain_name = (row[3])
            username = (row[4])
            account_id = (row[5])
            domain_id = (row[6])
            first_name = (row[7])
            last_name = (row[8])
            email = (row[9])

        con.commit()

        Cloudstack_Tests.api_key = api_key_rs
        Cloudstack_Tests.secret_key = secret_key_rs

        Cloudstack_Tests.sqlupdate.tbl_accounts(account_id, account_name, domain_id, domain_name, username, first_name, last_name, email)

    def testaccount_specific(self, t_apikey, t_secretkey):

        sql_host, sql_user, sql_password, sql_database = None, None, None, None
        values = DbConfig.objects.filter(db_purpose='cloudstack').values()

        for v in values:
            dict_values = v
        for k, v in dict_values.iteritems():
            if k == 'sql_host' : sql_host = v
            if k == 'sql_user' : sql_user = v
            if k == 'sql_password' :  sql_password = v
            if k == 'sql_database' :  sql_database = v

        con = mdb.connect(sql_host, sql_user, sql_password, sql_database);
        cursor = con.cursor()
        sql = "select cu.api_key, cu.secret_key, ca.account_name, cd.name, cu.username, \
                ca.id, cd.id, cu.firstname, cu.lastname, cu.email \
                from cloud.account ca \
                join cloud.user cu on cu.account_id = ca.id \
                join cloud.domain cd on cd.id = ca.domain_id \
                where cu.api_key = %s and cu.secret_key = %s"

        params = (t_apikey, t_secretkey)
        cursor.execute(sql, params)

        rows = cursor.fetchall()

        api_key_rs, secret_key_rs, account_name, domain_name, username, account_id, domain_id, first_name, last_name, email  \
        = None, None, None, None, None, None, None, None, None, None

        for row in rows:

            api_key_rs = (row[0])
            secret_key_rs = (row[1])
            account_name = (row[2])
            domain_name = (row[3])
            username = (row[4])
            account_id = (row[5])
            domain_id = (row[6])
            first_name = (row[7])
            last_name = (row[8])
            email = (row[9])

        con.commit()

        Cloudstack_Tests.api_key = api_key_rs
        Cloudstack_Tests.secret_key = secret_key_rs

        Cloudstack_Tests.sqlupdate.tbl_accounts(account_id, account_name, domain_id, domain_name, username, first_name, last_name, email)

    def listaccounts(self, api_key, secret_key):

        # We always start off a function by setting the cs_api to the CloudstackAPI 
        # class imported from cloudstackapi (see import at top)

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
        
        # Cloudstack API call - listAccounts
    
        listaccounts = cs_api.request(dict({'command':'listAccounts'}))
        listaccounts = dotdictify(listaccounts)
        listaccounts = listaccounts.listaccountsresponse.account

        for key, value in listaccounts[0].iteritems():
                print key, value


    def deployvm(self, t_serviceoffering, t_templatename, t_zone):
        
        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
        
        # Cloudstack API call - deployVirtualMachine

        depvm = cs_api.request(dict({'command':'deployVirtualMachine', 'serviceofferingid': t_serviceoffering, 'templateid': t_templatename, 'zoneid': t_zone}))
        depvm = dotdictify(depvm)
        depvm = depvm.deployvirtualmachineresponse

        asnycjob = None

        for key, value in depvm.items():
            if key == 'jobid' : asyncjob = value
                
        job = CloudstackAPI()
        job.asyncresults(asyncjob,api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Once the async job has completed, we then grab the vmid of the virtualmachine that has been created. We use this throughout the remainder of the script

        depvm_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        depvm_asyncqry = dotdictify(depvm_asyncqry)
        depvm_asyncqry = depvm_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        r_testname = 'r_deployvm'
        t_testname = 't_deployvm'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

                # Setting some variables for the deployvm output values to insert in to the deployvm table

        vmid, name, displayname, state, cpunumber, cpuspeed, memory, guestosid, templatename, hypervisor, \
        serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, created, resource_id, nic \
        = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        for key, value in depvm_asyncqry.iteritems():

            if key == 'name' : name = value
            if key == 'displayname' : displayname = value
            if key == 'state' : state = value
            if key == 'cpunumber' : cpunumber = value
            if key == 'cpuspeed' : cpuspeed = value
            if key == 'memory' : memory = value
            if key == 'guestosid' : guestosid = value
            if key == 'templatename' : templatename = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'serviceofferingid' : serviceofferingid = value
            if key == 'serviceofferingname' : serviceofferingname = value
            if key == 'serviceofferingname' : Cloudstack_Tests.vmso = value
            if key == 'guestosid' : ostypeid = value # also used when creating a template
            if key == 'guestosid' : Cloudstack_Tests.ostypeid = value # also used when creating a template
            if key == 'created' : created = value
            if key == 'id' : vmid = value # used for assigning various api calls
            if key == 'id' : Cloudstack_Tests.vmid = value
            if key == 'id' : resource_id = value # used in the db for cleanup purposes
            nic = None
            if key == 'nic' :
                nic = value
                for key, value in nic[0].iteritems():
                    if key == 'ipaddress' : ipaddress = value
                    if key == 'gateway' : gateway = value
                    if key == 'id' : networkid = value

        Cloudstack_Tests.sqlupdate.tbl_deployvm(vmid, name, displayname, state, cpunumber, cpuspeed, memory, \
        guestosid, templatename, hypervisor, serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, created, resource_id)


    def resetvmpw(self):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
    
        resetpasswd =  cs_api.request(dict({'command':'resetPasswordForVirtualMachine', 'id' : Cloudstack_Tests.vmid }))
        resetpasswd = dotdictify(resetpasswd)
        resetpasswd = resetpasswd.resetpasswordforvirtualmachineresponse

        asyncjob = None

        for key, value in resetpasswd.items():
            if key == 'jobid' : asyncjob = value
            print key, value

        job = CloudstackAPI()
        job.asyncresults(asyncjob=value,api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        resetpasswd_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        resetpasswd_asyncqry = dotdictify(resetpasswd_asyncqry)
        resetpasswd_asyncqry = resetpasswd_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        vmid, vmname, displayname, templatename, serviceofferingid, password, passwordenabled, aysncjob \
        = None, None, None, None, None, None, None, None

        for key, value in resetpasswd_asyncqry.iteritems():
            if key == 'id' : vmid = value
            if key == 'name' : vmname = value
            if key == 'displayname' : displayname = value
            if key == 'templatename' : templatename = value
            if key == 'serviceofferingid' : serviceofferingid = value
            if key == 'password' : password = value
            if key == 'passwordenabled' : passwordenabled = value

        r_testname = 'r_resetvwpw'
        t_testname = 't_resetvwpw'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        Cloudstack_Tests.sqlupdate.tbl_resetvmpw(vmid, vmname, displayname, templatename, serviceofferingid, password, passwordenabled, asyncjob)


    def changevmso(self, soid):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        vmid = Cloudstack_Tests.vmid
        newso = None
        oldso = Cloudstack_Tests.vmso
        
        changeso =  cs_api.request(dict({'command':'changeServiceForVirtualMachine', 'id' : vmid, 'serviceOfferingId' : soid }))
        changeso = dotdictify(changeso)
        changeso = changeso.changeserviceforvirtualmachineresponse

        r_testname = 'r_changesoforvm'
        t_testname = 't_changesoforvm'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        changeso_results = dotdictify(changeso)
        changeso_results = changeso_results.virtualmachine

        for key, value in  changeso_results.iteritems():

            if key == 'serviceofferingname' : newso = value

        Cloudstack_Tests.sqlupdate.tbl_changevmso(vmid, newso, oldso)

    def sourcenat_id(self):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        listpublicipaddresses = cs_api.request(dict({'command' : 'listPublicIpAddresses' }))
        listpublicipaddresses = dotdictify(listpublicipaddresses)
        listpublicipaddresses = listpublicipaddresses.listpublicipaddressesresponse.publicipaddress

        # Finding the sourcenat ID

        x = 0
        source_ipid = None
        sourcenat = False
        while sourcenat == False:
            for key, value in listpublicipaddresses[x].iteritems():
                if key == 'issourcenat' and value == True: sourcenat = True
                if key == 'id' : source_ipid = value
    
        Cloudstack_Tests.sourcenat_id = source_ipid
        
        return source_ipid
        
    def assign_ip(self, t_zone, iprole): # Assign IP function get acquire and IP to use for LB, Port Forwarding or Static NAT. Reusable function

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Creating local function variable

        Cloudstack_Tests.iprole = iprole # This variable is set when the function is called. This variable is used to describe what the assign_ip function will be used for (Static NAT / LB / PF)

        # Cloudstack API call - associateIpAddress

        assign_ip = cs_api.request(dict({'command':'associateIpAddress', 'zoneid': t_zone}))
        assign_ip = dotdictify(assign_ip)
        assign_ip = assign_ip.associateipaddressresponse

        asyncjob = None

        for key, value in assign_ip.items():
            if key == 'jobid': asyncjob = value

        # Checking asnyc job

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        assign_ip_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        assign_ip_asyncqry = dotdictify(assign_ip_asyncqry)
        assign_ip_asyncqry = assign_ip_asyncqry.queryasyncjobresultresponse.jobresult.ipaddress

        # The account now has an available public IP address to use that is not yet enabled for static NAT. Enable static NAT and create firewall policies

        ipid, publicipaddress, resource_id = None, None, None

        for key, value in assign_ip_asyncqry.items():

            if key == 'id' : ipid = value
            if key == 'id' : Cloudstack_Tests.pub_ipid = value
            if key == 'id' : resource_id = value
            if key == 'ipaddress' : publicipaddress = value
            iprole = iprole

        Cloudstack_Tests.sqlupdate.tbl_associateip(ipid, publicipaddress, iprole, resource_id)


    def enable_staticnat(self, t_zone, t_fwportfrom, t_fwportto, t_fwprotocol): # Enable static NAT - need to acquire an IP first using assign_ip function

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing and setting variables to execute the enableStaticNat API call
        
        pub_ipid = Cloudstack_Tests.pub_ipid
        vmid = Cloudstack_Tests.vmid
        ipid = Cloudstack_Tests.pub_ipid #duplicated code. We should change this to use pub_ipid. Change needs to follow through to Cloudstack_Tests.sqlupdate
        natstatus = 'failed'
        resourceid = Cloudstack_Tests.pub_ipid
        
        # Cloudstack API call - enableStaticNat

        enable_nat = cs_api.request(dict({'command':'enableStaticNat', 'ipaddressid':pub_ipid, 'virtualmachineid' : vmid }))
        time.sleep(15) # I find that the call is async so we hold here for a while to ensure that the static NAT call (line above) is done. This is different behaviour to the other api calls
        enable_nat = dotdictify(enable_nat)
        enable_nat = enable_nat.enablestaticmatresponse

        for key, value in enable_nat.iteritems():
            if key == 'success' : natstatus = 'success'

        create_staticnatpwrule = cs_api.request(dict({'command' : 'createIpForwardingRule' , 'ipaddressid' : pub_ipid , 'startport' : t_fwportfrom , \
                                            'endport' : t_fwportto , 'protocol' : t_fwprotocol }))
        create_staticnatpwrule = dotdictify(create_staticnatpwrule)
        create_staticnatpwrule = create_staticnatpwrule.createipforwardingruleresponse

        asyncvalue = None

        for key, value in create_staticnatpwrule.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        create_staticnatpwrule_asyncquery = cs_api.request(dict({'command' : 'queryAsyncJobResult', 'jobid' : asyncjob}))
        create_staticnatpwrule_asyncquery = dotdictify(create_staticnatpwrule_asyncquery)
        create_staticnatpwrule_asyncquery = create_staticnatpwrule_asyncquery.queryasyncjobresultresponse.jobresult.ipforwardingrule

        r_testname = 'r_enablestaticnat'
        t_testname = 't_enablestaticnat'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        publicendport, privateendport, protocol, state = None, None, None, None
   
        for key, value in create_staticnatpwrule_asyncquery.items():

            if key == 'startport' : publicendport = value
            if key == 'endport' : privateendport = value
            if key == 'protocol' : protocol = value
            if key == 'state' : state = value

        Cloudstack_Tests.sqlupdate.tbl_staticnat(ipid, vmid, natstatus, publicendport, privateendport, protocol, state, resourceid)
    
    def portforward(self, t_pfprivateport, t_pfpublicport, pfportprotocol): # Enable port forwarding rule. We will use the source NAT for the port forwarding rule

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)        

        # Grabbing variables to execute the enableStaticNat API call

        pub_ipid = Cloudstack_Tests.pub_ipid # we don't actually use this variable. We could do if we gave the option to create the port forward oe a new IP address
        vmid = Cloudstack_Tests.vmid
        
        # Cloudstack API call - listpublicipaddresses - used to get sourcenat ID

        listpublicipaddresses = cs_api.request(dict({'command' : 'listPublicIpAddresses' }))
        listpublicipaddresses = dotdictify(listpublicipaddresses)
        listpublicipaddresses = listpublicipaddresses.listpublicipaddressesresponse.publicipaddress

        # Finding the sourcenat ID

        x = 0
        source_ipid = None
        sourcenat = False
        while sourcenat == False:
            for key, value in listpublicipaddresses[x].iteritems():
                if key == 'issourcenat' and value == True: sourcenat = True
                if key == 'id' :
                    source_ipid = value

        # We have the sourcenat ID - we can now set up the port forwarding

        createportfw = cs_api.request(dict({'command':'createPortForwardingRule', 'ipaddressid' : source_ipid, 'protocol': pfportprotocol, \
                                                        'privateport': t_pfprivateport, 'publicport' : t_pfpublicport, 'virtualmachineid': vmid }))
        createportfw = dotdictify(createportfw)
        createportfw = createportfw.createportforwardingruleresponse

        asyncjob = None

        for key, value in createportfw.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Cloudstack API call - createportfw_result

        createportfw_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob})) 
        createportfw_asyncqry = dotdictify(createportfw_asyncqry)
        createportfw_asyncqry = createportfw_asyncqry.queryasyncjobresultresponse.jobresult.portforwardingrule


        r_testname = 'r_createipforwarder'
        t_testname = 't_createipforwarder'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        ipid , pubstartport, pubendport, privstartport, privendport, state, protocol, vmname, vmid, resource_id, jobstatus \
        = None, None, None, None, None, None, None, None, None, None, None

        for key, value in createportfw_asyncqry.iteritems():
            if key == 'ipaddressid' : ipid = value
            if key == 'publicport' : pubstartport = value
            if key == 'publicendport' : pubendport = value
            if key == 'privateport' : privstartport = value
            if key == 'privateendport' : privendport = value
            if key == 'state' : state = value
            if key == 'protocol' : protocol = value
            if key == 'virtualmachinename' : vmname = value
            if key == 'virtualmachineid' : vmid = value
            if key == 'id' : resource_id = value

        Cloudstack_Tests.sqlupdate.tbl_portfwrule(ipid , pubstartport, pubendport, privstartport, privendport, state, protocol, vmname, vmid, resource_id, jobstatus)

    def lb_rule(self, t_lpprivateport, t_lppublicport):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the createLoadBalancerRule API call

        vmid = Cloudstack_Tests.vmid
        pub_ipid = Cloudstack_Tests.pub_ipid

        name = ('LB rule using Public IP ID ' +str(pub_ipid))
        
        # Cloudstack API call - createLoadBalancerRule

        create_lbrule = cs_api.request(dict({'command':'createLoadBalancerRule', 'algorithm': 'roundrobin', 'name': name, 'privateport': t_lpprivateport, \
                                             'publicport' : t_lppublicport, 'publicipid': pub_ipid }))
        create_lbrule = dotdictify(create_lbrule)
        create_lbrule = create_lbrule.createloadbalancerruleresponse

        asyncjob = None

        for key, value in create_lbrule.items():
            if key == 'jobid': asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        create_lbrule_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        create_lbrule_asyncqry = dotdictify(create_lbrule_asyncqry)
        create_lbrule_asyncqry = create_lbrule_asyncqry.queryasyncjobresultresponse.jobresult.loadbalancer


        algorithm, ipid, publicipaddress, privateport, publicport, lbvmid, lbid, resource_id, jobstatus \
        = None, None, None, None, None, None, None, None, None
                                
        for key, value in create_lbrule_asyncqry.iteritems():
                                    
            if key == 'algorithm' : algorithm = value
            if key == 'publicipid' : ipid = value
            if key == 'publicip' : publicipaddress = value
            if key == 'privateport' : privateport = value
            if key == 'publicport' : publicport = value
            if key == 'id' : resource_id = value
            if key == 'id' : lbid = value

        Cloudstack_Tests.lbid = lbid

        assign_vm_to_lbrule = cs_api.request(dict({'command':'assignToLoadBalancerRule', 'id': lbid , 'virtualmachineids': vmid}))
        assign_vm_to_lbrule = dotdictify(assign_vm_to_lbrule)
        assign_vm_to_lbrule = assign_vm_to_lbrule.assigntoloadbalancerruleresponse

        for key, value in assign_vm_to_lbrule.items():
            if key == 'jobid': asyncjob = value

        assign_vm_to_lbrule_asyncqry = job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
        assign_vm_to_lbrule_asyncqry = dotdictify(assign_vm_to_lbrule_asyncqry)
        assign_vm_to_lbrule_asyncqry = assign_vm_to_lbrule_asyncqry.queryasyncjobresultresponse.jobresult

        r_testname = 'r_createlb'
        t_testname = 't_createlb'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)


        for key, value in assign_vm_to_lbrule_asyncqry.iteritems():
            if key == 'success':
                jobstatus = '1'
                lbvmid = vmid
            if value == 'false':
                jobstatus = '2'
                lbvmid = None

        Cloudstack_Tests.sqlupdate.tbl_lbrule(algorithm, ipid, publicipaddress, privateport, publicport, lbvmid, resource_id, jobstatus)


    def enablevpn(self):
    
        addvpnuser = Cloudstack_Tests.addvpnuser    
        sourcenat_id = Cloudstack_Tests.sourcenat_id
        vpnuser = None

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        enablevpn = cs_api.request(dict({'command':'createRemoteAccessVpn', 'publicipid' : sourcenat_id }))
        enablevpn = dotdictify(enablevpn)
        enablevpn = enablevpn.createremoteaccessvpnresponse

        asyncjob = None

        for key, value in enablevpn.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        enablevpn_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        enablevpn_asyncqry = dotdictify(enablevpn_asyncqry)
        enablevpn_asyncqry = enablevpn_asyncqry.queryasyncjobresultresponse.jobresult.remoteaccessvpn

        asyncjob = None

        if addvpnuser == 'vpnuser':
            
            addvpnusr = cs_api.request(dict({'command':'addVpnUser', 'username' : addvpnuser, 'password' : 'djsai38428u90dasnsjkldna' }))
            addvpnusr = dotdictify(addvpnusr)
            addvpnusr = addvpnusr.addvpnuserresponse
            
            for key, value in addvpnusr.items():
                if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        addvpnuser_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        addvpnuser_asyncqry = dotdictify(addvpnuser_asyncqry)
        addvpnuser_asyncqry = addvpnuser_asyncqry.queryasyncjobresultresponse.jobresult.vpnuser
        
        vpnuser = 'failed'
       
        for key, value in addvpnuser_asyncqry.iteritems():
            if key == 'username' : vpnuser = 'success'

        r_testname = 'r_enablevpn'
        t_testname = 't_enablevpn'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)


        for key, value in enablevpn_asyncqry.iteritems():

            if key == 'publicip' : publicip = value
            if key == 'publicipid' : pub_ipid = value
            if key == 'iprange' : iprange = value
            if key == 'presharedkey' : presharedkey = value
            if key == 'account' : account = value
            if key == 'state' : state = value
            if key == 'publicipid' : resource_id = value

        Cloudstack_Tests.sqlupdate.tbl_enablevpn( publicip, pub_ipid, iprange, presharedkey, account, state, addvpnuser, vpnuser, asyncjob, resource_id)

    def snapshot_vol(self, vol, r_testname, t_testname):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Cloudstack API call - listVolumes

        listvolumes = cs_api.request(dict({'command':'listVolumes'}))
        listvolumes = dotdictify(listvolumes)
        listvolumes = listvolumes.listvolumesresponse.volume

        x=0
        disk = None
        rootvol_id = None

        while disk != 'found' : 

            for key, value in listvolumes[x].iteritems():
        
                if key == 'id' : rootvol_id = value
                if key == 'type' and value == vol : disk = 'found'
                x =+1
       
        # Cloudstack API call - createSnapshot

        createsnap = cs_api.request(dict({'command' : 'createSnapshot', 'volumeid' : rootvol_id}))
        createsnap = dotdictify(createsnap)
        createsnap = createsnap.createsnapshotresponse

        asyncjob = None

        for key, value in createsnap.items():
                            
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        createsnap_asyncqry = cs_api.request(dict({'command' : 'queryAsyncJobResult', 'jobid' : asyncjob}))
        createsnap_asyncqry = dotdictify(createsnap_asyncqry)
        createsnap_asyncqry = createsnap_asyncqry.queryasyncjobresultresponse.jobresult.snapshot


        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)


        snapshotname, volumename, created, volumeid, snapshottype, resource_id = None, None, None, None, None, None

        for key, value in createsnap_asyncqry.iteritems():

            if key == 'name' : snapshotname = value
            if key == 'volumename' : volumename = value
            if key == 'created' : created = value
            if key == 'volumeid' : volumeid = value
            if key == 'snapshottype' : snapshottype = value
            if key == 'id' : resource_id = value
            if key == 'id' : Cloudstack_Tests.snap_id = value
        
        Cloudstack_Tests.sqlupdate.tbl_createsnapshot(snapshotname, volumename, created, volumeid, snapshottype, resource_id)


    def createtemplate(self, r_testname, t_testname):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # We need to grab the variables from other functions so we can execute the createTemplate API call.

        snap_id = Cloudstack_Tests.snap_id
        ostypeid = Cloudstack_Tests.ostypeid
        templatename = 'TemplateFromSnapshotid : '+str(snap_id)                            
        
        # Cloudstack API call - createTemplate

        createtemp = cs_api.request(dict({'command': 'createTemplate', 'name': templatename, 'displaytext': 'MyTemplate', \
                                                              'ostypeid':ostypeid, 'snapshotid': snap_id  }))
        createtemp = dotdictify(createtemp)
        createtemp = createtemp.createtemplateresponse

        asyncjob = None

        for key, value in createtemp.items():
            if key == 'jobid' : asyncjob = value
        
        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        createtemp_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        createtemp_asyncqry = dotdictify(createtemp_asyncqry)
        createtemp_asyncqry = createtemp_asyncqry.queryasyncjobresultresponse.jobresult.template
                
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)
                            
        displayname, templatetype, status, file_type, isfeatured, sourcetemplateid, templatename, hypervisor, resource_id \
        = None, None, None, None, None, None, None, None, None
                                    
        for key, value in createtemp_asyncqry.items():

            if key == 'displaytext' : displaytext = value
            if key == 'templatetype' : templatetype = value
            if key == 'status' : status = value
            if key == 'format' : file_type = value
            if key == 'isfeatured' : isfeatured = value
            if key == 'sourcetemplateid' : sourcetemplateid = value
            if key == 'name' : templatename = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'id' : resource_id = value
            if key == 'id' : Cloudstack_Tests.snaptemplate_id = value

        Cloudstack_Tests.sqlupdate.tbl_createtemplate(displayname, templatetype, status, file_type, isfeatured, sourcetemplateid, templatename, \
            hypervisor, resource_id)


    def depvm_rootsnap(self):      # deploy VM from the root snapshot

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute deployVitrualMachine from the template created from the snapshot

        so_id = Cloudstack_Tests.so_id
        zone_id = Cloudstack_Tests.zone_id
        snaptemp_id = Cloudstack_Tests.snaptemplate_id

        #Cloudstack API call - deployVirtualMachine

        depvmfromtemp = cs_api.request(dict({'command':'deployVirtualMachine', 'serviceofferingid': so_id, \
                                      'templateid': snaptemp_id, 'zoneid': zone_id}))
        depvmfromtemp = dotdictify(depvmfromtemp)
        depvmfromtemp = depvmfromtemp.deployvirtualmachineresponse

        aysncjob = None

        for key, value in depvmfromtemp.items():
            if key == 'jobid':
                asyncjob = value
        
        job = CloudstackAPI() 
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        depvmfromtemp_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        depvmfromtemp_asyncqry = dotdictify(depvmfromtemp_asyncqry)
        depvmfromtemp_asyncqry = depvmfromtemp_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        # Setting some variables for the deployvm output values to insert in to the deployvm table

        vmid, name, displayname, state, cpunumber, cpuspeed, memory, guestosid, templatename, hypervisor, \
        serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, guestosid, created, resource_id \
        = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        r_testname = 'r_deployvmfromsnap'
        t_testname = 't_deployvmfromsnap'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        for key, value in depvmfromtemp_asyncqry.iteritems():

            if key == 'name' : name = value
            if key == 'displayname' : displayname = value
            if key == 'state' : state = value
            if key == 'cpunumber' : cpunumber = value
            if key == 'cpuspeed' : cpuspeed = value
            if key == 'memory' : memory = value
            if key == 'guestosid' : guestosid = value
            if key == 'templatename' : templatename = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'serviceofferingid' : serviceofferingid = value
            if key == 'serviceofferingname' : serviceofferingname = value
            if key == 'guestosid': ostypeid = value # also used when creating a template
            if key == 'created' : created = value
            if key == 'id' : vmid = value
            if key == 'id' : Cloudstack_Tests.createtemp_vmid = value # set class function variable 
            if key == 'id' : resource_id = value # used in the db for cleanup purposes
            if key == 'nic':
                nic = value
                for key, value in nic[0].iteritems():
                    if key == 'ipaddress' : ipaddress = value
                    if key == 'gateway' : gateway = value
                    if key == 'id' : networkid = value

        Cloudstack_Tests.sqlupdate.tbl_deployvm(vmid, name, displayname, state, cpunumber, cpuspeed, memory, guestosid, templatename, \
                                                hypervisor, serviceofferingid, serviceofferingname, ipaddress, gateway, networkid, \
                                                created, resource_id)


    def create_vol(self, t_datavolserviceoffering, r_testname, t_testname): # Create a volume. Once the volume is created, it can then be attached

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the createVolume

        zone_id = Cloudstack_Tests.zone_id 

        # If the t_datavolserviceoffering value is snap_id, then we are creating a volume from a template that originated from a snapshot of the data volume 
        # We are reusing this function for 2 similar tests

        createvolapicmd = 'diskofferingid'
        if t_datavolserviceoffering == 'snap_id' : 
            t_datavolserviceoffering = Cloudstack_Tests.snap_id
            createvolapicmd = 'snapshotid'

        # Cloudstack API call - createVolume
        
        createvol = cs_api.request(dict({'command':'createVolume', 'name':'data', createvolapicmd:t_datavolserviceoffering, 'zoneid': zone_id}))
        createvol = dotdictify(createvol)
        createvol = createvol.createvolumeresponse

        asyncjob = None

        for key, value in createvol.items():
            if key == 'jobid' : asyncjob = value
        
        job = CloudstackAPI() 
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        createvol_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        createvol_asyncqry = dotdictify(createvol_asyncqry)
        createvol_asyncqry = createvol_asyncqry.queryasyncjobresultresponse.jobresult.volume

        diskname, extractable, state, disktype, size, diskofferingid, resource_id \
        = None, None, None, None, None, None, None

        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        for key, value in createvol_asyncqry.items():
            
            if key == 'name' : diskname = value
            if key == 'isextractable' : extractable = value
            if key == 'state' : state = value
            if key == 'type' : disktype = value
            if key == 'size' : size = value
            if key == 'diskofferingid' : diskofferingid = value
            if key == 'id' : resource_id = value
            if key == 'id' : Cloudstack_Tests.datavol_id = value # Set class variables

        Cloudstack_Tests.sqlupdate.tbl_createvol(diskname, extractable, state, disktype, size, diskofferingid, resource_id)


    def attach_vol(self, r_testname, t_testname): # Attach the volume created in the create_vol function

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the attachVolume API call

        datavol_id = Cloudstack_Tests.datavol_id
        vmid = Cloudstack_Tests.vmid

        # Cloudstack API call - attachVolume

        attachvol = cs_api.request(dict({'command':'attachVolume', 'id':datavol_id, 'virtualmachineid': vmid}))
        attachvol = dotdictify(attachvol)
        attachvol = attachvol.attachvolumeresponse

        async_job = None

        for key, value in attachvol.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        attachvol_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        attachvol_asyncqry = dotdictify(attachvol_asyncqry)
        attachvol_asyncqry = attachvol_asyncqry.queryasyncjobresultresponse.jobresult.volume

        
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)


        vmname, storage, state, vmid, created, attached, diskofferingid, vmstate, hypervisor, resource_id \
        = None, None, None, None, None, None, None, None, None, None

        for key, value in attachvol_asyncqry.items():

            if key == 'vmname' : vmname = value
            if key == 'storage' : storage = value
            if key == 'state' : state = value
            if key == 'virtualmachineid' : vmid = value
            if key == 'created' : created = value
            if key == 'attached' : attached = value
            if key == 'diskofferingid' : diskofferingid = value
            if key == 'vmstate' : vmstate = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'id' : resource_id = value

        Cloudstack_Tests.sqlupdate.tbl_attachvol(vmname, storage, state, vmid, created, attached, diskofferingid, vmstate, hypervisor, resource_id)


    def detach_vol(self, r_testname, t_testname):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the detachVolume API call

        datavol_id = Cloudstack_Tests.datavol_id

        # Cloudstack API call - detachVolume

        detach_data_vol = cs_api.request(dict({'command':'detachVolume' , 'id' : datavol_id }))
        detach_data_vol = dotdictify(detach_data_vol)
        detach_data_vol = detach_data_vol.detachvolumeresponse
        
        asyncjob = None

        for key, value in detach_data_vol.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        detach_data_vol_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        detach_data_vol_asyncqry = dotdictify(detach_data_vol_asyncqry)
        detach_data_vol_asyncqry = detach_data_vol_asyncqry.queryasyncjobresultresponse.jobresult.volume

        diskname, detached, disktype, storage, hypervisor, disksize, resource_id \
        = None, None, None, None, None, None, None 

        r_testname = 'r_detachdatavol'
        t_testname = 't_detachdatavol'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        for key, value in detach_data_vol_asyncqry.iteritems():

            if key == 'name' : diskname = value
            if key != 'attached' : detached = 'success'
            if key == 'type' : disktype = value
            if key == 'storage' : storage = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'size' : disksize = value
            if key == 'id' : resource_id = value
            detachedtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        Cloudstack_Tests.sqlupdate.tbl_detachvol(diskname, detached, detachedtime, disktype, storage, hypervisor, disksize, resource_id)


    def extract_vol(self, t_zone, r_testname, t_testname):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        data_vol = Cloudstack_Tests.datavol_id

        # Cloudstack API call - extractVolume

        extractvol = cs_api.request(dict({'command' : 'extractVolume' , 'id' : data_vol , 'mode' : 'HTTP_DOWNLOAD' , 'zoneid' : t_zone }))
        extractvol = dotdictify(extractvol)
        extractvol = extractvol.extractvolumeresponse

        asyncjob = None

        for key, value in extractvol.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        extractvol_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        extractvol_asyncqry = dotdictify(extractvol_asyncqry)
        extractvol_asyncqry = extractvol_asyncqry.queryasyncjobresultresponse.jobresult.volume # need to find out async repsonse json tags

        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)        


        extractmode, dwnlstate, url, volnamedownloaded, resource_id = None, None, None, None, None

        for key, value in extractvol_asyncqry.iteritems():
            if key == 'extractMode' : extractmode = value
            if key == 'state' : dwnlstate = value
            if key == 'url' : url = value
            if key == 'name' : volnamedownloaded = value
            if key == 'id' : resource_id = value
        
        Cloudstack_Tests.sqlupdate.tbl_downloadvol(extractmode, dwnlstate, url, volnamedownloaded, resource_id)

        # need to pass values to database - need to create tables in cloud_tests_db 


    def stop_vm(self):
        
        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the stopVirtualMachine API call 

        vmid = Cloudstack_Tests.vmid

        # Cloudstack API call - stopVirtualMachine

        stopvm = cs_api.request(dict({'command' : 'stopVirtualMachine' , 'id' : vmid }))
        stopvm = dotdictify(stopvm)
        stopvm = stopvm.stopvirtualmachineresponse
        
        asyncjob = None

        for key, value in stopvm.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        stopvm_asyncqry = cs_api.request(dict({'command' : 'queryAsyncJobResult', 'jobid' : asyncjob}))
        stopvm_asyncqry = dotdictify(stopvm_asyncqry)
        stopvm_asyncqry = stopvm_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        stoptime, vmname, hypervisor, resource_id, attachediso, isoid, isoname = None, None, None, None, None, None, None

        for key , value in stopvm_asyncqry.iteritems():
           
            stoptime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            if key == 'name' : vmname = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'id' : resource_id = value
            if key == 'isoid' : attachediso = 'Y'
            if key == 'isoid' : isoid = value
            if key == 'isoname' : isoname = value

        Cloudstack_Tests.sqlupdate.tbl_stopvm(stoptime, vmname, hypervisor, resource_id, attachediso, isoid, isoname)

        # just sleeping for 1 min to give the vm a chance to reboot correctly
        time.sleep(60)


    def start_vm(self, r_testname, t_testname):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the startVirtualMachine API call

        vmid = Cloudstack_Tests.vmid

        # Cloudstack API call - startVirtualMachine

        startvm = cs_api.request(dict({'command' : 'startVirtualMachine' , 'id' : vmid }))
        startvm = dotdictify(startvm)
        startvm = startvm.startvirtualmachineresponse

        aysncjob = None

        for key, value in startvm.items():
            if key == 'jobid' : asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        startvm_asyncqry = cs_api.request(dict({'command' : 'queryAsyncJobResult', 'jobid' : asyncjob}))
        startvm_asyncqry = dotdictify(startvm_asyncqry)
        startvm_asyncqry = startvm_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        if r_testname != None:
            x = Cloudstack_Tests()
            x.update_test_results(r_testname, t_testname)

        starttime, vmname, hypervisor, resource_id, attachediso, isoid, isoname = None, None, None, None, None, None, None
                
        for key , value in startvm_asyncqry.iteritems():
           
            starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            if key == 'name' : vmname = value
            if key == 'hypervisor' : hypervisor = value
            if key == 'id' : resource_id = value
            if key == 'isoid' : attachediso = 'Y'
            if key == 'isoid' : isoid = value
            if key == 'isoname' : isoname = value

        Cloudstack_Tests.sqlupdate.tbl_startvm(starttime, vmname, hypervisor, resource_id, attachediso, isoid, isoname)
         
        # just sleeping for 1 min to give the vm a chance to reboot correctly
        time.sleep(60)

    def reboot_vm(self, r_testname, t_testname):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the rebootVirtualMachine API call

        vmid = Cloudstack_Tests.vmid

        # Cloudstack API call - rebootVirtualMachine

        rebootvm = cs_api.request(dict({'command' : 'rebootVirtualMachine' , 'id' : vmid }))
        rebootvm = dotdictify(rebootvm)
        rebootvm = rebootvm.rebootvirtualmachineresponse

        asyncjob = None

        for key, value in rebootvm.items():
            if key == 'jobid' : asyncjob = value
        
        job = CloudstackAPI()
        job.asyncresults(asyncjob=value, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        rebootvm_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        rebootvm_asyncqry = dotdictify(rebootvm_asyncqry)
        rebootvm_asyncqry = rebootvm_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        vmname, vmid, attachediso, reboottime = None, None, None, None

        for key, value in rebootvm_asyncqry.iteritems():
            if key == 'name' : vmname = value
            if key == 'id' : vmid = value
            if key == 'isoname' : attachediso = value
            reboottime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        Cloudstack_Tests.sqlupdate.tbl_rebootvm(vmname, vmid, attachediso, reboottime)

        # just sleeping for 1 min to give the vm a chance to reboot correctly
        time.sleep(60)

    def attach_iso(self):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the rebootVirtualMachine API call

        vmid = Cloudstack_Tests.vmid

        # Cloudstack API call - List ISOs

        listallisos = cs_api.request(dict({'command' : 'listIsos'}))
        listallisos = dotdictify(listallisos)
        listallisos = listallisos.listisosresponse.iso

        x = 0
        isoqry = False
        isoid = None
        while isoqry != 'xen-pv-drv-iso':

            for key, value in listallisos[x].iteritems():

                if key == 'id' : isoid = value
                if key == 'displaytext' and value == 'xen-pv-drv-iso': isoqry = 'xen-pv-drv-iso'
                x = +1

        attiso = cs_api.request(dict({'command' : 'attachIso' , 'id' : isoid , 'virtualmachineid' : vmid }))
        attiso = dotdictify(attiso)
        attiso = attiso.attachisoresponse

        asyncjob = None

        for key, value in attiso.items():
            if key == 'jobid': asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
        

        attiso_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        attiso_asyncqry = dotdictify(attiso_asyncqry)
        attiso_asyncqry = attiso_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        
        r_testname = 'r_attachiso'
        t_testname = 't_attachiso'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        isoid, isoname, vmname, vmid, resource_id = None, None, None, None, None

        for key, value in attiso_asyncqry.iteritems():
            if key == 'isoid' : isoid = value
            if key == 'isoname' : isoname = value
            if key == 'name' : vmname = value
            if key == 'id' : vmid = value
            if key == 'id' : resource_id = value

        Cloudstack_Tests.sqlupdate.tbl_attachiso(isoid, isoname, vmname, vmid, resource_id)

    def detach_iso(self):

        cs_api = CloudstackAPI(api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        # Grabbing variables to execute the rebootVirtualMachine API call

        vmid = Cloudstack_Tests.vmid

        detachiso = cs_api.request(dict({'command' : 'detachIso' , 'virtualmachineid' : vmid }))
        detachiso = dotdictify(detachiso)
        detachiso = detachiso.detachisoresponse

        asyncjob = None

        for key, value in detachiso.items():
            if key == 'jobid': asyncjob = value

        job = CloudstackAPI()
        job.asyncresults(asyncjob, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

        detachiso_asyncqry = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        detachiso_asyncqry = dotdictify(detachiso_asyncqry)
        detachiso_asyncqry = detachiso_asyncqry.queryasyncjobresultresponse.jobresult.virtualmachine

        r_testname = 'r_detachiso'
        t_testname = 't_detachiso'
        x = Cloudstack_Tests()
        x.update_test_results(r_testname, t_testname)

        isodetached, vmname, vmid, detachedtime = None, None, None, None

        for key ,value in detachiso_asyncqry.iteritems():

            if key != 'isoname' : isodetached = 'success'
            if key == 'name' : vmname = value
            if key == 'id' : vmid = value
            detachedtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        Cloudstack_Tests.sqlupdate.tbl_detachiso(isodetached, vmname, vmid, detachedtime)

    def update_test_results(self, r_testname, t_testname):

        jobresult = None
        job = CloudstackAPI()
        jobresult_int = job.jobresults
        
        if str(jobresult_int) == '1': jobresult = 'success'
        if str(jobresult_int) == '2': jobresult = 'failed'
        testid = Cloudstack_Tests.sqlupdate.tbl_test_nameid
        Cloudstack_Tests.sqlupdate.tbl_test_criteria_status(r_testname, t_testname, jobresult, testid)

    def intialise_test(self, t_csmip, t_testaccount, t_listaccount, t_apikey, t_secretkey, t_serviceoffering, t_templatename, \
                        t_zone, t_resetvwpw, t_changesoforvm, t_changevmso, t_stopstartvm, t_rebootvm, t_enablevpn, t_addvpnuser, \
                        t_enablestaticnat, t_fwportfrom, t_fwportto, t_fwprotocol, t_createipforwarder, t_pfprivateport, t_pfpublicport, \
                        t_pfportprotocol, t_createlb, t_lpprivateport, t_lppublicport, t_snaprootvol, t_createtempfromsnap, t_deployvmfromsnap, \
                        t_attachdatadatavol, t_datavolserviceoffering, t_createsnapfromdatavol, t_createtempfromdatavolsnap, \
                        t_createvolfromsnapshot, t_attachsnapvol, t_detachdatavol, \
                        t_extractdatavol, t_attachiso, t_rebootvmwiso, t_stopstartvmwiso, t_detachiso, t_uploadiso, t_pathtoiso, t_attachuploadediso, \
                        t_detachuploadediso, t_extractuploadediso, t_deleteresource ):

        
        # Setting the cloudstack Management IP address using t_csmip which is passed by POST and appending the port value (currently a static value)
       
        csmhost = t_csmip
        csmport = ':8080'
        csmip = csmhost+csmport
        
        # Setting class variables to use to initiate tests, for example, deploy_vm will use these variables.

        Cloudstack_Tests.so_id = t_serviceoffering
        Cloudstack_Tests.template_id = t_templatename
        Cloudstack_Tests.zone_id = t_zone

        # Get acocunt information and API & secret keys. Api and secret keys are then set as class variables, Cloudstack_Tests.xxxx.

        test = Cloudstack_Tests()

        if t_testaccount == 'random':
            
            test.testaccount_random()
        
        if t_testaccount == 'list':
            
            test.testaccount_list(t_listaccount)
        
        if t_testaccount == 'specific':
            
            test.testaccount_specific(t_apikey, t_secretkey)

        # Deploy virtual machine using deplyoyvm function and variables

        test.deployvm(t_serviceoffering, t_templatename, t_zone)

        # Basic test to stop and start VM.

        if t_stopstartvm == True:
            
            test.stop_vm()
            r_testname = 'r_stopstartvm'
            t_testname = 't_stopstartvm'
            test.start_vm(r_testname, t_testname)

        # Basic test to reboot the VM

        if t_rebootvm == True:
            
            r_testname = 'r_rebootvm'
            t_testname = 't_rebootvm'
            test.reboot_vm(r_testname, t_testname)

        if t_resetvwpw == True:
            
            test.stop_vm()
            test.resetvmpw()
            
            # setting testname parameters to None for starting VM. Stop / start is part of the iniated test, ie reest password requires the machine to be stopped
            test.start_vm(r_testname=None, t_testname=None)

        # Change service offering for vmirtual machine

        if t_changesoforvm == True:
            
            test.stop_vm()
            test.changevmso(t_changevmso)

            # setting testname parameters to None for starting VM. Stop / start is part of the iniated test, ie chaging the SO for the VM  requires the machine to be stopped
            test.start_vm(r_testname=None, t_testname=None)

        # Enable a static NAT. First we assign an IP address, then enable a static nat on the IP address to the vm deployed as part of the test

        if t_enablestaticnat == True:
            
            iprole = 'StaticNat'
            test.assign_ip(t_zone, iprole)
            test.enable_staticnat(t_zone, t_fwportfrom, t_fwportto, t_fwprotocol)

        # Create a port forward rule - this port forward IP rul is done on the source nat to the vm deployed as part of the test

        if t_createipforwarder == True:
            
            test.portforward(t_pfprivateport, t_pfpublicport, t_pfportprotocol)

        # Create a LB rul on the vm deployed as part of the test. We obtain a public IP address for the LB rule

        if t_createlb == True:
            
            iprole = 'LoadBalancer'
            test.assign_ip(t_zone, iprole)
            test.lb_rule(t_lpprivateport, t_lppublicport)

        # Create VPN on source NAT

        if t_addvpnuser == True:
            
            Cloudstack_Tests.addvpnuser = 'vpnuser'

        if t_enablevpn == True:
            
            test.sourcenat_id()
            test.enablevpn()

        # Snapshot the root volume of the VM deployed as part of the test

        if t_snaprootvol == True:
            
            vol = 'ROOT'
            r_testname = 'r_snaprootvol'
            t_testname = 't_snaprootvol'
            test.snapshot_vol(vol, r_testname, t_testname)

            # Create a template from the root volume snapshot

            if t_createtempfromsnap == True:
                
                r_testname = 'r_createtempfromsnap'
                t_testname = 't_createtempfromsnap'
                test.createtemplate(r_testname, t_testname)    

                # Deploy a VM from the root volume snapshot template

                if t_deployvmfromsnap == True:
                    
                    test.depvm_rootsnap()  # We could reuse the deployvm() function. We would use less cose ~30-40 lines of code.. it IS working as stands.

        # Create and attach and data volume

        if t_attachdatadatavol == True:
           
            # Create the volume first
 
            r_testname = 'r_createdatavol'
            t_testname = 't_createdatavol'
            test.create_vol(t_datavolserviceoffering, r_testname, t_testname)
            
            r_testname = 'r_attachdatadatavol'
            t_testname = 't_attachdatadatavol'
            test.attach_vol(r_testname,t_testname)
            
            # Create a snapshot from the attached data volume

            if t_createsnapfromdatavol == True:
                
                vol = 'DATADISK'
                r_testname = 'r_createsnapfromdatavol'
                t_testname = 't_createsnapfromdatavol'
                test.snapshot_vol(vol, r_testname, t_testname)

                # Create a template from snapshot of the data volume

                if t_createtempfromdatavolsnap == True:
                    
                    r_testname = 'r_createtempfromdatavolsnap'
                    t_testname = 't_createtempfromdatavolsnap'
                    test.createtemplate(r_testname, t_testname) 

                if t_createvolfromsnapshot == True:
                    
                    t_datavolserviceoffering = 'snap_id'    
                    r_testname = 'r_createvolfromsnapshot'
                    t_testname = 't_createvolfromsnapshot'
                    test.create_vol(t_datavolserviceoffering, r_testname, t_testname)

                if t_attachsnapvol == True:
                    
                    r_testname = 'r_attachsnapvol'
                    t_testname = 't_attachsnapvol'
                    test.attach_vol(r_testname, t_testname)        

        if t_detachdatavol == True:
                
            r_testname = 'r_detachdatavol'
            t_testname = 't_detachdatavol'    
            test.detach_vol(r_testname, t_testname)

        if t_extractdatavol == True:
                
            r_testname = 'r_extractdatavol'
            t_testname = 't_extractdatavol'    
            test.extract_vol(t_zone, r_testname, t_testname)

        #if t_createsnapfromdatavol == True
        #    test.

        if t_attachiso == True:
            
            test.attach_iso()
            
            # Reboot VM with ISO attached

            if t_rebootvmwiso == True:
                
                r_testname = 'r_rebootvmwiso'
                t_testname = 't_rebootvmwiso'
                test.reboot_vm(r_testname, t_testname)

            # Stop and start with ISO attached
            
            if t_stopstartvmwiso == True:
                
                test.stop_vm()
                
                # setting tesname parameters for when the ISO is attached
                
                r_testname = 'r_stopstartvmwiso'
                t_testname = 't_stopstartvmwiso'
                test.start_vm(r_testname, t_testname)
                

            if t_detachiso == True:
                
                test.detach_iso()


        test_id = Cloudstack_Tests.sqlupdate.tbl_test_nameid

        if t_deleteresource == False:
           
            #setting instance to access remove_resource 
            x = deleteresources
        
            # Destroying VMs
            resource = 'destroyVirtualMachine'
            x.remove_resource(resource, test_id, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
            
            # removing public IPs acquired
            resource = 'disassociateIpAddress'
            x.remove_resource(resource, test_id, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

            # removing snapshots created
            resource = 'deleteSnapshot'
            x.remove_resource(resource, test_id, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
            
            # removing volumes created
            resource = 'deleteVolume'
            x.remove_resource(resource, test_id, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

            # removing templates created
            resource = 'deleteTemplate'
            x.remove_resource(resource, test_id, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)

            # removing VPN on source NAT
            resource = 'deleteRemoteAccessVpn'
            x.remove_resource(resource, test_id, api_key=Cloudstack_Tests.api_key, secret_key=Cloudstack_Tests.secret_key)
