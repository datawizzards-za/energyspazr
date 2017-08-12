$(document).ready(function(){
    var table_all_quote = $('#table_all_quotes').DataTable();
    
    $('#system_details').hide();
    $('#client_details').hide();
    $('#quotes_stats').hide();
    
    var order = null;
    var client = null;
    var order_num = null;
    var system_order = null;
    var system_type = null;

    $('#table_all_quotes tbody').on( 'click', 'tr', function (e) {
        var row = $('tr', this);
        
        order_num = $('td', this).eq(0).text();
        
        var system_order_url = 'app/api/get_systemorder_details/' + order_num + '/';
        $.ajax({
           url: system_order_url,
           type: 'GET',
           async: false,
           success: function (data){
               system_order = data[0];
           }
        });
        
        $('#order_number').text(system_order.order_number);
        $('#need_finance').text(system_order.need_finance);
        
        if (!system_order.geyser[0]){
            $('#intended_use').text(system_order.pvt[0].intended_use);
            $('#site_visit').text(system_order.pvt[0].site_visit);
            $('#property_type').text(system_order.pvt[0].property_type);
            $('#roof_inclination').text(system_order.pvt[0].roof_inclination);
            
            $('#_number').hide();
            $('#_size').hide();
            $('#_collector').hide();
        }else{
            $('#users_number').text(system_order.geyser[0].users_number);
            $('#required_geyser_size').text(system_order.geyser[0].required_geyser_size);
            $('#property_type').text(system_order.geyser[0].property_type);
            $('#roof_inclination').text(system_order.geyser[0].roof_inclination);
            $('#water_collector').text(system_order.geyser[0].water_collector);
            
            $('#_use').hide();
            $('#_visit').hide();
        }
                
        var order_url = 'app/api/get_order_details/' + system_order.order_number + '/';
        $.ajax({
           url: order_url,
           type: 'GET',
           async: false,
           success: function (data){
               order = data[0];
           }
        });
        
        var client_url = 'app/api/get_client_details/' + order.client + '/';
        $.ajax({
           url: client_url,
           type: 'GET',
           async: false,
           success: function (data){
               client = data[0];
           }
        });
        
        var address_url = 'app/api/get_client_address/' + client.physical_address_id + '/';
        $.ajax({
           url: address_url,
           type: 'GET',
           async: false,
           success: function (data){
               address = data[0];
           }
        });
        
        $('#c_names').text(client.firstname + ' ' + client.lastname);
        $('#c_email').text(client.username);
        $('#c_contact_number').text(client.contact_number);
        $('#a_building_name').text(address.building_name);
        $('#a_street_name').text(address.street_name);
        $('#a_suburb').text(address.suburb);
        $('#a_city').text(address.city + ', ' + address.zip_code);
        
        var province_url = 'app/api/get_prov_name/' + address.province_id + '/';
        $.ajax({
           url: province_url,
           type: 'GET',
           async: false,
           success: function (data){
               province = data[0];
           }
        });
        
        $('#a_province').text(province.name);
        
        $('#all_quotes').hide();
        
        $('#system_details').show();
        $('#client_details').show();
        $('#quotes_stats').show();
    });
});
