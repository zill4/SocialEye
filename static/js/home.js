
/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        // Attempt add read for brands.
        'b_read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/brand',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_b_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/people',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(fname, lname) {
            let ajax_options = {
                type: 'POST',
                url: 'api/people',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'fname': fname,
                    'lname': lname
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        // attempt create for brands
        b_create: function(bname) {
            let ajax_options = {
                type: 'POST',
                url: 'api/brand',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'bname': bname
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_b_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        ba_create: function(asin) {
            let ajax_options = {
                type: 'POST',
                url: 'api/brand/' + asin,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'asin': asin
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_b_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(fname, lname) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/people/' + lname,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'fname': fname,
                    'lname': lname
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        b_update: function(bname) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/brand/' + bname,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'bname': bname,
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_b_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'b_delete': function(bname) {
            let bname2 = bname.getElementById('bname').value;
            console.log(bname2);
            
            let ajax_options = {
                type: 'DELETE',
                url: 'api/brand/' + bname2,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_b_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/people/' + lname,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
// Updated for brands
ns.view = (function() {
    'use strict';

    let $fname = $('#fname'),
        $lname = $('#lname');
    // Attempt for Brand
    let $bname = $('#bname');
//  Not in use...
//        $asin = $('#asin');
    // return the API
    return {
        reset: function() {
            $lname.val('');
            $fname.val('').focus();
            //attempt for brand
            $bname.val('').focus();
        },
        update_editor: function(fname, lname) {
            $lname.val(lname);
            $fname.val(fname).focus();
        },
        //attempt for brand
        update_beditor: function(bname){
            $bname.val(bname).focus();
        },
        build_table: function(people) {
            let rows = ''

            // clear the table
            $('.people table > tbody').empty();

            // did we get a people array?
            if (people) {
                for (let i=0, l=people.length; i < l; i++) {
                    rows += `<tr><td class="fname">${people[i].fname}</td><td class="lname">${people[i].lname}</td><td>${people[i].timestamp}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        // attempt for brand build table
        build_btable: function(brand) {
            let rows = ''

            // clear the table
            $('.brand table > tbody').empt();
            
            // did we get a brand array?
            if (brand) {
                for (let i=0, l=brand.length; i < l; i++){
                    rows += `<tr><td class="bname">${brand[i].bname}</td><td>${brand[i].timestamp}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $fname = $('#fname'),
        $lname = $('#lname'),
        // attempt add for brands.
        $bname = $('#bname'),
        $asin = $('#asin');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
        // Attempt to add b_read to function timeout.
        model.b_read();
    }, 100)


    // Validate input
    function validate(fname, lname) {
        return fname !== "" && lname !== "";
    }
    // Attempt validate brand name
    function bvalidate(bname){
        return bname !== "";
    }
    // Attempt validate asin
    function bavalidate(asin){
        return asin !== "";
    }
    // Create our event handlers
    $('#create').click(function(e) {
        let fname = $fname.val(),
            lname = $lname.val();

        e.preventDefault();

        if (validate(fname, lname)) {
            model.create(fname, lname)
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let fname = $fname.val(),
            lname = $lname.val();

        e.preventDefault();

        if (validate(fname, lname)) {
            model.update(fname, lname)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let lname = $lname.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(lname)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            fname,
            lname;

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        view.update_editor(fname, lname);
    });
    // Attempt to add brand event hendlers

// Create our event handlers
$('#b_create').click(function(e) {
    let bname = $bname.val();

    e.preventDefault();

    if (bvalidate(bname)) {
        model.b_create(bname)
    } else {
        alert('Problem with brand name input');
    }
});
$('#ba_create').click(function(e) {
    let asin = $asin.val();

    e.preventDefault();

    if (bavalidate(asin)) {
        model.ba_create(asin)
    } else {
        alert('Problem with asin input');
    }
});

$('#b_update').click(function(e) {
    let bname = $bname.val();

    e.preventDefault();

    if (bvalidate(bname)) {
        model.b_update(bname)
    } else {
        alert('Problem with brand name input');
    }
    e.preventDefault();
});

$('#b_delete').click(function(e) {
    let bname = $bname.val();

    e.preventDefault();

    if (bvalidate('placeholder', bname)) {
        model.b_delete(lname)
    } else {
        alert('Problem with brand name input');
    }
    e.preventDefault();
});

// $('#b_reset').click(function() {
//     view.b_reset();
// })

$('table > tbody').on('dblclick', 'tr', function(e) {
    let $target = $(e.target),
        bname;

    bname = $target
        .parent()
        .find('td.bname')
        .text();
    view.update_beditor(bname);
});
// End of brand event handlers.

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });
    
    // Attempt to add brand model events

    $event_pump.on('model_b_read_success', function(e, data){
        view.build_btable(data);
        view.reset();
    });

    $event_pump.on('model_b_create_success', function(e, data){
        model.b_read();
    });
    
    $event_pump.on('model_b_update_success', function(e, data){
        model.b_read();
    });

    $event_pump.on('model_b_delete_success', function(e, data){
        model.b_read();
    })
    // End of brand events
    
    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
