from django.db import connections

def Accounts():

    rsAccounts = []

    cursor = connections['cloudstack'].cursor()
    cursor.execute("SELECT account_name, account_name FROM cloud.account where type <> '1' and state = 'enabled' and account_name <> 'vmturbo' order by account_name;")
    accounts = cursor.fetchall()

    for v in accounts[::]:

        rsAccounts.append(v)

    return rsAccounts
    cursor.close()


def ServiceOfferings():

    rsServiceOfferings = []

    cursor = connections['cloudstack'].cursor()
    cursor.execute("select id, name from cloud.disk_offering where removed is null and system_use <> '1' and type = 'Service' order by id desc;")
    serviceofferings = cursor.fetchall()

    for v in serviceofferings[::]:

        rsServiceOfferings.append(v)

    return rsServiceOfferings
    cursor.close()

def Zones():

    rsZones = []

    cursor = connections['cloudstack'].cursor()
    cursor.execute("SELECT id, name FROM cloud.data_center WHERE removed is null;")
    zones = cursor.fetchall()


    for v in zones[::]:

        rsZones.append(v)
        
    return rsZones
    cursor.close()

def DiskOfferings():

    rsDiskOfferings = []

    cursor = connections['cloudstack'].cursor()
    cursor.execute("select id, name from cloud.disk_offering where removed is null and system_use <> '1' and type = 'Disk';")
    diskofferings = cursor.fetchall()

    for v in diskofferings[::]:

        rsDiskOfferings.append(v)

    return rsDiskOfferings
    cursor.close()

def PublicTemplates():

    rsPublicTemplates = []

    cursor = connections['cloudstack'].cursor()
    cursor.execute("select id, name from cloud.vm_template where public = '1' and featured ='1' and removed is null and type = 'USER';")
    publictemplates = cursor.fetchall()

    for v in publictemplates[::]:

        rsPublicTemplates.append(v)

    return rsPublicTemplates
    cursor.close()



