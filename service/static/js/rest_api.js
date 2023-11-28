$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_quantity").val(res.quantity);
        $("#product_restock_level").val(res.restock_level);
        $("#product_restock_count").val(res.restock_count);
        $("#product_condition").val(res.condition);
        $("#product_first_entry_date").val(res.first_entry_date);
        $("#product_last_restock_date").val(res.last_restock_date);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_quantity").val("");
        $("#product_restock_level").val("");
        $("#product_restock_count").val("");
        $("#product_condition").val("Unknown");
        $("#product_first_entry_date").val("");
        $("#product_last_restock_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let quantity = $("#product_quantity").val();
        let restock_level = $("#product_restock_level").val();
        let restock_count = $("#product_restock_count").val();
        let condition = $("#product_condition").val()=="UNKNOWN"?null:$("#product_condition").val();
        let first_entry_date = $("#product_first_entry_date").val();
        let last_restock_date = $("#product_last_restock_date").val();

        let data = {
            "id":product_id,
            "name": name,
            "quantity": quantity,
            "restock_level": restock_level,
            "restock_count": restock_count,
            "condition":condition,
            "first_entry_date": first_entry_date,
            "last_restock_date": last_restock_date,
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/inventory",
            contentType: "application/json",
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let quantity = $("#product_quantity").val();
        let restock_level = $("#product_restock_level").val();
        let restock_count = $("#product_restock_count").val();
        let condition = $("#product_condition").val()=="UNKNOWN"?null:$("#product_condition").val();
        let first_entry_date = $("#product_first_entry_date").val();
        let last_restock_date = $("#product_last_restock_date").val();

        let data = {
            "id":product_id,
            "name": name,
            "quantity": quantity,
            "restock_level": restock_level,
            "restock_count": restock_count,
            "condition":condition,
            "first_entry_date": first_entry_date,
            "last_restock_date": last_restock_date,
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/inventory/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Restock a Product
    // ****************************************

    $("#restock-btn").click(function () {

        let product_id = $("#product_id").val();
        //$("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/inventory/${product_id}/restock`,
                contentType: "application/json",
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/inventory/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });


    

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/inventory/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let quantity = $("#product_quantity").val();
        let restock_level = $("#product_restock_level").val();
        let restock_count = $("#product_restock_count").val();
        let condition = $("#product_condition").val()=="UNKNOWN"?null:$("#product_condition").val();
        let first_entry_date = $("#product_first_entry_date").val();
        let last_restock_date = $("#product_last_restock_date").val();

        let queryString = ""

        if(product_id){
            queryString += 'id=' + product_id
        }

        if (name) {
            if (queryString.length > 0) {
                queryString += '&name=' + quantity
            } else {
                queryString += 'name=' + name
            }
        }
        if (quantity) {
            if (queryString.length > 0) {
                queryString += '&quantity=' + quantity
            } else {
                queryString += 'quantity=' + quantity
            }
        }
        // if (restock_level) {
        //     if (queryString.length > 0) {
        //         queryString += '&restock_level=' + restock_level
        //     } else {
        //         queryString += 'restock_level=' + restock_level
        //     }
        // }

        // if (restock_count) {
        //     if (queryString.length > 0) {
        //         queryString += '&restock_count=' + restock_count
        //     } else {
        //         queryString += 'restock_count=' + restock_count
        //     }
        // }

        if (condition) {
            if (queryString.length > 0) {
                queryString += '&condition=' + condition
            } else {
                queryString += 'condition=' + condition
            }
        }

        // if (first_entry_date) {
        //     if (queryString.length > 0) {
        //         queryString += '&first_entry_date=' + first_entry_date
        //     } else {
        //         queryString += 'first_entry_date=' + first_entry_date
        //     }
        // }
        // if (last_restock_date) {
        //     if (queryString.length > 0) {
        //         queryString += '&last_restock_date=' + last_restock_date
        //     } else {
        //         queryString += 'last_restock_date=' + last_restock_date
        //     }
        // }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/inventory?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Restock Level</th>'
            table += '<th class="col-md-2">Restock Count</th>'
            table += '<th class="col-md-2">Condition</th>'
            table += '<th class="col-md-2">First Entry Date</th>'
            table += '<th class="col-md-2">Last Restock Date</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.quantity}</td><td>${product.restock_level}</td><td>${product.restock_count}</td><td>${product.condition}</td><td>${product.first_entry_date}</td><td>${product.last_restock_date}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
