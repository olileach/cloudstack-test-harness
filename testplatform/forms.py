from django.forms.fields import DateField, MultipleChoiceField
from django.contrib.admin import widgets 
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect

from django import forms
from testplatform.clouddb import Zones, ServiceOfferings, DiskOfferings, PublicTemplates, Accounts
from testplatform.models import CloudStackIpAddress


class TestCriteriaForm(forms.Form):

    XENVERSION = (
        ("56", "56"),
        ("56sp2", "56sp2"),
        ("any", "any version"),)

    PORTFORWRDPROTOCOLS = (
        ("TCP", "tcp"),
        ("UDP", "udp"),)

    TESTACCOUNT = (
        ("random", "generate a random account"),
        ("list", "select from drop down"),
        ("specific", "specify the secret and api key for a user"),)

    # Test name and number of accounts to loop through

    testname = forms.CharField(label='Test Name (required)', required=True, widget=forms.TextInput(attrs={'size': '40'}))
    csmip = forms.ModelChoiceField(queryset=CloudStackIpAddress.objects.all(), label='Cloudstack management server IP to test (required)') 
    
    # Test Xenserver Version.

    xenversion = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Select XenServer version to test against (required)", choices=XENVERSION, required=False)

    # Test account choice. Gives the user a choice of how to pick an account - random, from a list or specific user api and sceret key

    testaccount = forms.CharField(label="Choose a test account (required)", widget=forms.RadioSelect(choices=TESTACCOUNT), required=True)
    listaccount = forms.ChoiceField(choices=Accounts(), label='Account', required=False)
    apikey = forms.CharField(label='Account api key', max_length=86, required=False, widget=forms.TextInput(attrs={'size': '110'}))
    secretkey = forms.CharField(label='Account secret key', max_length=86, required=False, widget=forms.TextInput(attrs={'size':'110'}))

    # Deploy a VM

    serviceoffering = forms.ChoiceField(choices=ServiceOfferings(), label='Service Offering (required)', required=False)
    templatename = forms.ChoiceField(choices=PublicTemplates(), label='Template Name (required)', required=False)
    zone = forms.ChoiceField(choices=Zones(), label='Zones (required)', required=False)

    # Basic stop start and reboot

    stopstartvm = forms.BooleanField(label='Stop and Start VM', required=False)
    rebootvm = forms.BooleanField(label='Reboot VM', required=False)
    
    # Deploy VM options

    resetvwpw = forms.BooleanField(label='Reset VM password', required=False)
    changesoforvm = forms.BooleanField(label='Change Service Offering for VM', required=False)
    changevmso = forms.ChoiceField(choices=ServiceOfferings(), label='Service Offering', required=False) 
    
    # Static NAT options

    enablestaticnat = forms.BooleanField(label='Enable static NAT', required=False)
    fwportfrom = forms.DecimalField(label='FW port from:', min_value=1,max_value=65000,decimal_places=0, required=False)
    fwportto = forms.DecimalField(label='FW port to:', min_value=1,max_value=65000,decimal_places=0,
        error_messages={'error': 'You cannot enter decimal places for a firewall port'}, required=False)
    fwprotocol = forms.ChoiceField(choices=PORTFORWRDPROTOCOLS, label='Protocol for static nat', required=False)

    # Load balancer options

    createipforwarder = forms.BooleanField(label='Create IP forwarding rule', required=False)
    pfprivateport = forms.DecimalField(label='Forward private port:', min_value=1,max_value=65000,decimal_places=0, required=False)
    pfpublicport = forms.DecimalField(label='To public port:', min_value=1,max_value=65000,decimal_places=0, required=False)     
    pfportprotocol = forms.ChoiceField(choices=PORTFORWRDPROTOCOLS, label='Protocol', required=False)
    
    # Load balancer options

    createlb = forms.BooleanField(label='Create load balancer', required=False)
    lpprivateport = forms.DecimalField(label='LB private port:', min_value=1,max_value=65000,decimal_places=0, required=False)
    lppublicport = forms.DecimalField(label='LB public port:', min_value=1,max_value=65000,decimal_places=0, required=False)    

    # Enable VPN on source NAT

    enablevpn = forms.BooleanField(label='Enable VPN on source NAT', required=False)
    addvpnuser = forms.BooleanField(label='Add a user to the VPN', required=False)
    
    # Create snapshot of root volume

    snaprootvol = forms.BooleanField(label='Snapshot root volume', required=False)
    createtempfromsnap = forms.BooleanField(label='Create template from root snapshot', required=False)
    deployvmfromsnap = forms.BooleanField(label='Deploy VM from template', required=False)

    # Data volume tests

    attachdatadatavol = forms.BooleanField(label='Attach data volume to VM', required=False)
    datavolserviceoffering = forms.ChoiceField(choices=DiskOfferings(), label='Select data volume size', required=False)
    createsnapfromdatavol = forms.BooleanField(label='Create snapshot from data volume', required=False)
    createtempfromdatavolsnap = forms.BooleanField(label='Create template from data volume snapshot', required=False)
    createvolfromsnapshot = forms.BooleanField(label='Create a volume from the snapshot', required=False)
    attachsnapvol = forms.BooleanField(label='Attach snapshot volume to VM', required=False)
    detachdatavol = forms.BooleanField(label='Detach data volume', required=False)
    extractdatavol = forms.BooleanField(label='Extract data volume', required=False)

    # ISO tests

    attachiso = forms.BooleanField(label='Attach an ISO', required=False)
    rebootvmwiso = forms.BooleanField(label='Reboot VM with ISO attached', required=False)
    stopstartvmwiso = forms.BooleanField(label='Stop and start VM with ISO attached', required=False)
    detachiso = forms.BooleanField(label='Detach an ISO', required=False)
    uploadiso = forms.BooleanField(label='Upload an ISO', required=False)
    pathtoiso = forms.URLField(required=False, label='Upload URL path for ISO')
    attachuploadediso = forms.BooleanField(label='Attach uploaded ISO', required=False)
    detachuploadediso = forms.BooleanField(label='Detach uploaded ISO', required=False)
    extractuploadediso = forms.BooleanField(label='Extract uploaded ISO', required=False)

    # Clean up resource

    deleteresource = forms.BooleanField(label='Keep all resources created during the test', required=False)

    # Email test results

    email = forms.EmailField(label='Email when test completes', required=False)
 
    def clean_changevmso(self):
        cd = self.cleaned_data

        changesoforvm = cd.get('changesoforvm')
        changevmso = cd.get('changevmso')
        serviceoffering = cd.get('serviceoffering')

        if changesoforvm == True:
            if changevmso == serviceoffering:

                raise forms.ValidationError("You have selected to change the service offering, but the service offering is the same value \
                                             as the service offering used when deploying the virtual machine. \
                                             Please change the service offering to a different value.")
        
        return changevmso
         
