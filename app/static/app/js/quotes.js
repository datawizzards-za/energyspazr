$(document).ready(function(){
    var table_all_quote = $('#table_all_quotes').DataTable();
    
    $('#system_details').hide();
    $('#client_details').hide();
    $('#quotes_stats').hide();
    
    var system_order = null;
    var order = null;
    var client = null;

    $('#table_all_quotes tbody').on( 'click', 'tr', function (e) {
        var row = $('tr', this);
        //var id = row.context.attributes[0].value;
        var order_num = $('td', this).eq(0).text();
        //var price = $('td', this).eq(1).text();
         //var title = this.parentNode.getElementsByTagName('td')[1].innerHTML;
        var system_order_url = 'app/api/get_sysorder_details/' + order_num + '/';
        $.ajax({
           url: system_order_url,
           type: 'GET',
           async: false,
           success: function (data){
               //console.log(data);
               system_order = data[0];
           }
        });
        
        var order_url = 'app/api/get_order_details/' + system_order.order_number + '/';
        $.ajax({
           url: order_url,
           type: 'GET',
           async: false,
           success: function (data){
               //console.log(data);
               order_url = data[0];
           }
        });
        
        var client_url = 'app/api/get_client_details/' + order_url.client + '/';
        $.ajax({
           url: client_url,
           type: 'GET',
           async: false,
           success: function (data){
               client = data[0];
           }
        });
        
        //console.log(client.physical_address);
        $('#c_firstname').text(client.firstname);
        $('#c_lastname').text(client.lastname);
        $('#c_username').text(client.username);
        $('#c_contact_number').text(client.contact_number);
        
        $('#all_quotes').hide();
        
        $('#system_details').show();
        $('#client_details').show();
        $('#quotes_stats').show();
    });
});
