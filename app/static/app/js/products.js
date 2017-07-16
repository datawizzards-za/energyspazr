$(document).ready(function(){
    var table_my_prods = $('#table_my_products').DataTable();
    var table_all_panels = $('#table_all_panels').DataTable();
    var table_all_prods = $('#table_all_products').DataTable();
    
    $('#add_new_product').hide();
    $('#add_products').hide();
    $('#all_panels').hide();
    $('#edit_panel').hide();
    $('#all_products').hide();

    $('#table_my_products tbody').on( 'click', 'tr', function (e) {
        var row = $('tr', this);
        var id = row.context.attributes[0].value;
        var name = $('td', this).eq(0).text();
        var price = $('td', this).eq(1).text();

        $('#edit_prod_name').val(name);
        $('#edit_prod_price').val(price);
        $('#id_edit_prod_id').val(id);

        $('#my_products').hide();
        $('#all_panels').show();
    });

    $('#table_all_panels tbody').on( 'click', 'tr', function (e) {
        //$(this).toggleClass('selected');
        var row = $('tr', this);
        var id = row.context.attributes[0].value;
        var name = $('td', this).eq(0).text();
        var price_text = $('td', this).eq(1).text();
        console.log(id +" "+ name +" "+price_text)
        /**
        //TODO: Replace 'R' with '' instead
        var price = price_text.substring(1, price_text.length).replace(',','');

        $('#edit_prod_name').val(name);
        $('#edit_prod_price').val(price);
        $('#id_edit_prod_id').val(id);

        $('#all_panels').hide();
        $('#edit_panel').show();*/
    });

    $('.panel-price').change(function(){
        var value = $(this).val(); 

        var test = parseFloat(value);

        console.log("Value: " + test);
    });
 

    $('#table_all_products tbody').on( 'click', 'tr', function (e) {
        var selected = $(this).attr('value');
        console.log(selected);

        switch(selected) {
            case 'Batteries':
                break;
            case 'Solar':
                $('#all_products').hide();
                $('#all_panels').show();
                break;

        }
    });

    $('#button').click( function () {
        alert( table.rows('.selected').data().length +' row(s) selected' );
    });
    
    $('#btn_add_products').click(
        function(){
            $('#btn_add_selected').addClass('disabled')
            $('#my_products').hide();
            $('#add_products').show();
        }
    );

    $('.btn_edit_product').click(
        function(){
            var name = $(this).closest('tr').find('td:nth-child(1)').text();
            var price_text = $(this).closest('tr').find('td:nth-child(2)').text();
            var price = price_text.substring(1, price_text.length).replace(',','');
            var id = $(this).closest('tr')[0].attributes[0].value;

            $('#edit_prod_name').val(name);
            $('#edit_prod_price').val(price);
            $('#id_edit_prod_id').val(id);

            $('#my_products').hide();
            $('#edit_product').show();
        }
    );

    $('#btn_panels_back').click(
        function(){
            $('#all_panels').hide();
            $('#all_products').show();
        }
    );

    $('#btn_add_new').click(
        function(){
            $('#all_products').hide();
            $('#add_new_product').show();
        }
    );

    $('#btn_add').click(
        function(){
            $('#my_products').hide();
            $('#all_products').show();
            //$('#add_products').show();
        }
    );
    
    $('#btn_products_back').click(
        function(){
            $('#all_products').hide();
            $('#my_products').show();
        }
    );
}); 
