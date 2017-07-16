$(document).ready(function(){
    var table_all_quote = $('#table_all_quotes').DataTable();
    
    var mydata = null;

    $('#table_all_quotes tbody').on( 'click', 'tr', function (e) {
        var row = $('tr', this);
        //var id = row.context.attributes[0].value;
        var order_num = $('td', this).eq(0).text();
        //var price = $('td', this).eq(1).text();
         //var title = this.parentNode.getElementsByTagName('td')[1].innerHTML;
        var url = 'app/api/get_order_details/' + order_num + '/';
        $.ajax({
           url: url,
           type: 'GET',
           async: false,
           success: function (data){
               //console.log(data);
               mydata = data[0];
           }
        });
         
        console.log(mydata);
         
         //console.log(order_num);
                
        //$('#edit_prod_name').val(name);
        //$('#edit_prod_price').val(price);
        //$('#id_edit_prod_id').val(id);

        //$('#my_products').hide();
        //$('#all_panels').show();
    });
    
    //console.log(mydata);
 
});
