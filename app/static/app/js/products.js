$(document).ready(function(){
    var table_my_prods = $('#table_my_products').DataTable();
    var table_all_prods = $('#table_all_products').DataTable();
    var table_all_panels = $('#table_all_panels').DataTable();
    window.product_name = null; 

    $('#add_new_product').hide();
    $('#add_products').hide();
    $('#all_panels').hide();
    $('#edit_panel').hide();
    $('#all_products').hide();

    $('#table_my_products tbody').on( 'dblclick', 'tr', function (e) {
        console.log("Double clicked");

        var tr = $(this).closest('tr');
        console.log(tr.children());
        /*
        var row = $('tr', this);
        var id = row.context.attributes[0].value;
        var name = $('td', this).eq(0).text();
        var price = $('td', this).eq(1).text();

        $('#edit_prod_name').val(name);
        $('#edit_prod_price').val(price);
        $('#id_edit_prod_id').val(id);

        $('#my_products').hide();
        $('#all_panels').show();
       */
    });

    $('#table_all_products tbody').on( 'click', 'tr', function (e) {
        var selected = parseInt($(this).attr('value'));
        setProductTable(selected-1);

        $('#all_products').hide();
        $('#all_panels').show();
        $('.panel-checked').hide();

        $('.panel-price').keyup(function(){
            var tr = $(this).closest('tr');
            var value = $(this).val(); 
            if (value == '') {
                tr.find('.panel-checked').hide();
                tr.find('.panel-unchecked').show();
                tr.removeClass('selected');
            }else{
                tr.find('.panel-unchecked').hide();
                tr.find('.panel-checked').show();
                tr.addClass('selected');
            }
        });
    });


    $('#btn_submit_panels').click(function(){
        var selected = $('#table_all_panels tbody').find('tr.selected');
        var length = selected.length;
        
        $.each(selected, function(i, elem){
            console.log("Button Clicked");
            var length = elem.children.length;
            var name = $('td', elem).eq(0).text();
            var csrftoken = getCookie('csrftoken');
            var dimensions = [];
            for (var i = 1; i < length-2; i++) {
                var value = $('td', elem).eq(i).text();
                var key = elem.closest('table').children[0].children[0].children[i].innerHTML;
                key = key.toLowerCase();
                dimensions.push([key, value]);
            }

            var price = $('td', elem).eq(length-2).find('input').val();
            var data = {'brand_name': name, 'dimensions': dimensions,
                        'price': price, 'csrfmiddlewaretoken': csrftoken,
                        'product': window.product_name};

            $.ajax({
                url:'/app/my-products/',
                method: 'POST',
                data: data,
                dataType: 'json',
                traditional: true,
            });
        });
        //location.reload();
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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

    function setProductTable(selected) {
        var table = $('#table_all_panels');
        table.empty();

        // Create table head
        var product = all_products[selected];
        window.product_name = product.brand__product;
        document.getElementById("product-head").innerHTML = 'Available ' + product.brand__product + 's';  
        var keys = Object.keys(product.dimensions);

        // Compile headers
        var thead = document.createElement('thead');
        var tr = document.createElement('tr');
        var product_name = product.brand__product.replace(" ","_").toLowerCase();

        $.each(keys, function(index, value) {
            data_field = product_name + "_" + value;
            var th = document.createElement('th');
            th.setAttribute('data-field', data_field);
            $(th).addClass("col-md-4 text-center");
            th.innerHTML = value.charAt(0).toUpperCase() + value.slice(1);
            tr.appendChild(th);
        });

        // Add Price column
        data_field = product_name + "_price";
        th = document.createElement('th');
        th.setAttribute('data-field', data_field);
        $(th).addClass("col-md-4 text-center");
        th.innerHTML = "Price";
        tr.appendChild(th);

        // Add Add column
        data_field = product_name + "_add";
        th = document.createElement('th');
        th.setAttribute('data-field', data_field);
        $(th).addClass("col-md-4 text-center");
        th.innerHTML = "Add";
        tr.appendChild(th);
        
        thead.appendChild(tr);

        var tbody = document.createElement('tbody');
        var values = [];
        for (var i = 0; i < product.pcount; i++) {
            values.push([]);
        }
        $.each(product.dimensions, function(key, value) {
            $.each(value, function(index, value) {
                values[index].push(value);
            });
        });

        for (var i = 0; i < values.length; i++) {
            tr = document.createElement('tr');
            for (var j = 0; j < values[i].length; j++) {
                var td = document.createElement('td');
                $(td).addClass("text-center");
                td.innerHTML = values[i][j];
                tr.append(td);
            }

            // Price Data
            td = document.createElement('td');
            $(td).addClass("text-center");
            var out_div = document.createElement('div');
            $(out_div).addClass("input-group form-group mb-2 mr-sm-2 mb-sm-0 has-danger")
            var inner_div = document.createElement('div');
            $(inner_div).addClass("input-group-addon");
            inner_div.innerHTML = "R";
            out_div.append(inner_div);
            var input = document.createElement('input');
            $(input).addClass("form-control panel-price");
            input.setAttribute("type", "number");
            input.setAttribute("step", 0.1);
            input.setAttribute("min", 0);
            input.setAttribute("placeholder", "Enter price e.g. 150.56");
            out_div.append(input);
            td.append(out_div);
            tr.append(td);

            // Add Data
            td = document.createElement('td');
            $(td).addClass("text-center");
            var icon1 = document.createElement('i'); 
            $(icon1).addClass("fa fa-close fa-2x panel-unchecked");
            td.append(icon1);
            var icon2 = document.createElement('i'); 
            $(icon2).addClass("fa fa-check fa-2x panel-checked");
            td.append(icon2);
            tr.append(td);

            tbody.append(tr);
        }

        table.append(thead);
        table.append(tbody);
    }
}); 
