$(function() {
    $('body').each(function() {
        var html = $(this).html();
            $(this).html(
            html.replace(/required/g, "<span style=\"color:#800517; font-weight: bold;\">required</span>")
        );
    });
});

    $(document).ready(function() {

        // clean up of checkboxes when checkboxes are hidden after being displayed
        
        $('#id_xenversion_0').change(function() {
            if ($(this).is(':checked')){
                $('input[id=id_xenversion_1]').attr('checked', false);
                $('input[id=id_xenversion_2]').attr('checked', false);
            }
        });

        $('#id_xenversion_1').change(function() {
            if ($(this).is(':checked')){
                $('input[id=id_xenversion_0]').attr('checked', false);
                $('input[id=id_xenversion_2]').attr('checked', false);
            }
        });

        $('#id_xenversion_2').change(function() {
            if ($(this).is(':checked')){
                $('input[id=id_xenversion_0]').attr('checked', false);
                $('input[id=id_xenversion_1]').attr('checked', false);
            }
        });

        $('#id_testaccount_2').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_apikey]').val('');
                $('input[id=id_secretkey]').val('');
            }
        });

        $('#id_snaprootvol').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_createtempfromsnap]').attr('checked', false);
                $('input[id=id_deployvmfromsnap]').attr('checked', false);
            }
        });

        $('#id_enablestaticnat').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_fwportfrom]').val('');
                $('input[id=id_fwportto]').val('');
            }
        });

        $('#id_createipforwarder').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_pfprivateport]').val('');
                $('input[id=id_pfpublicport]').val('');
            }
        });

        $('#id_createlb').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_lpprivateport]').val('');
                $('input[id=id_lppublicport]').val('');
            }
        });

        $('#id_enablevpn').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_addvpnuser]').attr('checked', false);
            }
        });

        $('#id_createtempfromsnap').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_deployvmfromsnap]').attr('checked', false);
            }
        });

        $('#id_attachdatadatavol').change(function() {
            if ($(this).not(':checked')){
                $("#id_datavolserviceoffering").val("---------");
                $('input[id=id_createsnapfromdatavol]').attr('checked', false);
                $('input[id=id_createtempfromdatavolsnap]').attr('checked', false);
                $('input[id=id_detachdatavol]').attr('checked', false);
                $('input[id=id_extractdatavol]').attr('checked', false);
                $('input[id=id_attachedsnapvol]').attr('checked', false);
            }
        });

        $('#id_createsnapfromdatavol').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_createtempfromdatavolsnap]').attr('checked', false);
                $('input[id=id_createvolfromsnapshot]').attr('checked', false);
            }
        });

        $('#id_createvolfromsnapshot').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_attachsnapvol]').attr('checked', false);
                $('input[id=id_attachsnapvol]').attr('checked', false);
            }
        });


        $('#id_detachdatavol').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_extractdatavol]').attr('checked', false);
            }
        });    

        $('#id_attachiso').change(function() {
            if ($(this).not(':checked')){
                $('input[id=id_rebootvmwiso]').attr('checked', false);
                $('input[id=id_stopstartvmwiso]').attr('checked', false);
                $('input[id=id_detachiso]').attr('checked', false);
            }
        });

        $('#id_uploadiso').change(function() {
            if ($(this).not(':checked')){
        
                $('input[id=id_pathtoiso]').val('http://');
                $('input[id=id_attachuploadediso]').attr('checked', false);
                $('input[id=id_detachuploadediso]').attr('checked', false);
                $('input[id=id_extractuploadediso]').attr('checked', false);
            }
        });

        $('#id_attachuploadediso').change(function() {
            if ($(this).not(':checked')){

                $('input[id=id_detachuploadediso]').attr('checked', false);
                $('input[id=id_extractuploadediso]').attr('checked', false);
            }
        });

        $('#id_detachuploadediso').change(function() {
            if ($(this).not(':checked')){

                $('input[id=id_extractuploadediso]').attr('checked', false);
            }
        });


    // end function
    });

    $(document).ready(function() {

        // hiding unrequired checkboxes when initial page loads  

        //test account options
        $('#id_listaccount, #id_apikey, #id_secretkey').hide();
        $("label[for='id_listaccount'], label[for='id_apikey'], label[for='id_secretkey']").hide();

        //service offering options
        $('#id_changevmso').hide();
        $("label[for='id_changevmso']").hide();
        
        //static nat options
        $('#id_fwportto, #id_fwportfrom, #id_fwprotocol').hide();
        $("label[for='id_fwportfrom'], label[for='id_fwportto'], label[for='id_fwprotocol']").hide();
        
        //port forwarding options
        $('#id_pfprivateport, #id_pfpublicport, #id_pfportprotocol').hide();
        $("label[for='id_pfprivateport'], label[for='id_pfpublicport'], label[for='id_pfportprotocol']").hide();

        //load balancer options
        $('#id_lpprivateport, #id_lppublicport').hide();
        $("label[for='id_lpprivateport'], label[for='id_lppublicport']").hide(); 

        //VPN options
        $('#id_addvpnuser').hide();
        $ ("label[for='id_addvpnuser']").hide();
        //snapshot options
        $('#id_createtempfromsnap, #id_deployvmfromsnap').hide();
        $("label[for='id_createtempfromsnap'], label[for='id_deployvmfromsnap']").hide();

        //volume options
        $('#id_datavolserviceoffering, #id_createsnapfromdatavol, #id_createtempfromdatavolsnap, #id_createvolfromsnapshot, #id_attachsnapvol, #id_detachdatavol, #id_extractdatavol').hide();
        $("label[for='id_datavolserviceoffering'], label[for='id_createsnapfromdatavol'], label[for='id_createtempfromdatavolsnap']").hide();
        $("label[for='id_createvolfromsnapshot'], label[for='id_attachsnapvol']").hide();
        $("label[for='id_detachdatavol'], label[for='id_extractdatavol']").hide();

        //attach ISO options
        $('#id_rebootvmwiso').hide();
        $("label[for='id_rebootvmwiso']").hide();
        $('#id_stopstartvmwiso').hide();
        $("label[for='id_stopstartvmwiso']").hide();        
        $('#id_detachiso').hide();
        $("label[for='id_detachiso']").hide();

        $('#id_pathtoiso').hide();
        $("label[for='id_pathtoiso']").hide();
        $('#id_attachuploadediso').hide();
        $("label[for='id_attachuploadediso']").hide();
        $('#id_detachuploadediso').hide();
        $("label[for='id_detachuploadediso']").hide();
        $('#id_extractuploadediso').hide();
        $("label[for='id_extractuploadediso']").hide();

        // due to the fact we can;t get the upload ISO working using the cloudstack API, we are hiding the upload ISO checkbox
        //
        $('#id_uploadiso').hide();
        $("label[for='id_uploadiso']").hide();
    });


    $(document).ready(function() {

    
        // Test account_0 options
        $('#id_testaccount_0').change(function() {
            if ($(this).is(':checked')){
                
                $('#id_listaccount, #id_apikey, #id_secretkey').hide();
                $("label[for='id_listaccount'], label[for='id_apikey'], label[for='id_secretkey']").hide();
            }
        });
        
        // Test account_1 options
        $('#id_testaccount_1').change(function() {
            if ($(this).is(':checked')){

                $('#id_listaccount').show();
                $("label[for='id_listaccount']").show();
                $('#id_apikey, #id_secretkey').hide();
                $("label[for='id_apikey'], label[for='id_secretkey']").hide();

            }
        });

        // Test account_2 options
        $('#id_testaccount_2').change(function() {
            if ($(this).is(':checked')){

                $('#id_apikey, #id_secretkey').show();
                $("label[for='id_apikey'], label[for='id_secretkey']").show();
                $('#id_listaccount').hide();
                $("label[for='id_listaccount']").hide();

            }
        });

        //service offering options
        //
        $('#id_changesoforvm').change(function() {
            if ($(this).is(':checked')){

                $('#id_changevmso').show();
                $("label[for='id_changevmso']").show();
            } else {

                $('#id_changevmso').hide();
                $("label[for='id_changevmso']").hide();
            }
        });


        //network options
        $('#id_enablestaticnat').change(function() {
            if ($(this).is(':checked')){
                
                $('#id_fwportto, #id_fwportfrom, #id_fwprotocol').show();
                $("label[for='id_fwportfrom'], label[for='id_fwportto'], label[for='id_fwprotocol']").show();
            } else {
                
                $('#id_fwportto, #id_fwportfrom, #id_fwprotocol').hide();
                $("label[for='id_fwportfrom'], label[for='id_fwportto'], label[for='id_fwprotocol']").hide();
            }
        });


        //port forwarding options

        $('#id_createipforwarder').change(function() {
            if ($(this).is(':checked')){
    
                $('#id_pfprivateport, #id_pfpublicport, #id_pfportprotocol').show();
                $("label[for='id_pfprivateport'], label[for='id_pfpublicport'], label[for='id_pfportprotocol']").show();
            } else {

                $('#id_pfprivateport, #id_pfpublicport, #id_pfportprotocol').hide();
                $("label[for='id_pfprivateport'], label[for='id_pfpublicport'], label[for='id_pfportprotocol']").hide();

            }
        }); 

        // create load balancer options

        $('#id_createlb').change(function() {
            if ($(this).is(':checked')){

                $('#id_lpprivateport, #id_lppublicport').show();
                $("label[for='id_lpprivateport'], label[for='id_lppublicport']").show();

            } else {

                $('#id_lpprivateport, #id_lppublicport').hide();
                $("label[for='id_lpprivateport'], label[for='id_lppublicport']").hide();
            }
        });


        $('#id_enablevpn').change(function() {
            if ($(this).is(':checked')){

                $('#id_addvpnuser').show();
                $("label[for='id_addvpnuser']").show();

            } else {

                $('#id_addvpnuser').hide();
                $("label[for='id_addvpnuser']").hide();
            }
        });


        //snapshot options
       $('#id_snaprootvol').change(function() {
            if ($(this).is(':checked')){
            
                $('#id_createtempfromsnap').show();
                $("label[for='id_createtempfromsnap']").show();
            
            } else { 

                $("label[for='id_createtempfromsnap']").hide();
                $('#id_createtempfromsnap').hide();
                $('#id_deployvmfromsnap').hide();
                $("label[for='id_deployvmfromsnap']").hide();
            }
        });

        $('#id_createtempfromsnap').change(function() {
            if ($(this).is(':checked')){
                                
                $('#id_deployvmfromsnap').show();
                $("label[for='id_deployvmfromsnap']").show();

            } else {
                
                $('#id_deployvmfromsnap').hide();
                $("label[for='id_deployvmfromsnap']").hide();

            }
        });

        //volume options
    
        $('#id_attachdatadatavol').change(function() {
            if ($(this).is(':checked')){
            
                $('#id_datavolserviceoffering').show();
                $("label[for='id_datavolserviceoffering']").show();
                $('#id_createsnapfromdatavol').show();
                $("label[for='id_createsnapfromdatavol']").show();
                $('#id_detachdatavol').show();
                $("label[for='id_detachdatavol']").show();
            
            } else {
            
                $('#id_datavolserviceoffering').hide();
                $("label[for='id_datavolserviceoffering']").hide();
                $('#id_createsnapfromdatavol').hide();
                $("label[for='id_createsnapfromdatavol']").hide();
                $('#id_createtempfromdatavolsnap').hide();
                $("label[for='id_createtempfromdatavolsnap']").hide();
                $('#id_createvolfromsnapshot').hide();
                $("label[for='id_createvolfromsnapshot']").hide();    
                $('#id_detachdatavol').hide();
                $("label[for='id_detachdatavol']").hide();
                $('#id_attachsnapvol').hide()
                $("label[for='id_attachsnapvol']").hide();;
                $('#id_extractdatavol').hide();
                $("label[for='id_extractdatavol']").hide();                
            }
        });


        $('#id_createsnapfromdatavol').change(function() {
            if ($(this).is(':checked')){

                $('#id_createtempfromdatavolsnap').show();
                $("label[for='id_createtempfromdatavolsnap']").show();
                $('#id_createvolfromsnapshot').show();
                $("label[for='id_createvolfromsnapshot']").show();

            } else {

                $('#id_createtempfromdatavolsnap').hide();
                $("label[for='id_createtempfromdatavolsnap']").hide();
                $('#id_createvolfromsnapshot').hide();
                $("label[for='id_createvolfromsnapshot']").hide();
                $('#id_attachsnapvol').hide();
                $("label[for='id_attachsnapvol']").hide();
            }
        });

        $('#id_createvolfromsnapshot').change(function() {
             if ($(this).is(':checked')){

                $('#id_attachsnapvol').show();
                $("label[for='id_attachsnapvol']").show();

            } else {

                $('#id_attachsnapvol').hide();
                $("label[for='id_attachsnapvol']").hide();

            }
        });

        
        $('#id_detachdatavol').change(function() {
            if ($(this).is(':checked')){
                
                $('#id_extractdatavol').show();
                $("label[for='id_extractdatavol']").show();

            } else {

                $('#id_extractdatavol').hide();
                $("label[for='id_extractdatavol']").hide();

            }
        });


        $('#id_attachiso').change(function() {
            if ($(this).is(':checked')){
                
                $('#id_rebootvmwiso').show();
                $("label[for='id_rebootvmwiso']").show();
                $('#id_stopstartvmwiso').show();
                $("label[for='id_stopstartvmwiso']").show();
                $('#id_detachiso').show();
                $("label[for='id_detachiso']").show();

            } else {

                $('#id_rebootvmwiso').hide();
                $("label[for='id_rebootvmwiso']").hide();
                $('#id_stopstartvmwiso').hide();
                $("label[for='id_stopstartvmwiso']").hide();
                $('#id_detachiso').hide();
                $("label[for='id_detachiso']").hide();
            }
        });

        $('#id_uploadiso').change(function() {
            if ($(this).is(':checked')){

                $('#id_pathtoiso').show();
                $("label[for='id_pathtoiso']").show();
                $('#id_attachuploadediso').show();
                $("label[for='id_attachuploadediso']").show();

            } else {

                $('#id_pathtoiso').hide();
                $("label[for='id_pathtoiso']").hide();
                $('#id_attachuploadediso').hide();
                $("label[for='id_attachuploadediso']").hide();
                $('#id_detachuploadediso').hide();
                $("label[for='id_detachuploadediso']").hide();
                $('#id_extractuploadediso').hide();
                $("label[for='id_extractuploadediso']").hide();

            }
        });

        $('#id_attachuploadediso').change(function() {
            if ($(this).is(':checked')){

                $('#id_detachuploadediso').show();
                $("label[for='id_detachuploadediso']").show();

            } else {

                $('#id_detachuploadediso').hide();
                $("label[for='id_detachuploadediso']").hide();
                $('#id_extractuploadediso').hide();
                $("label[for='id_extractuploadediso']").hide();
            }
        });



        $('#id_detachuploadediso').change(function() {
            if ($(this).is(':checked')){

                $('#id_extractuploadediso').show();
                $("label[for='id_extractuploadediso']").show();

            } else {

                $('#id_extractuploadediso').hide();
                $("label[for='id_extractuploadediso']").hide();

            }
        });            



// Close function
    });
