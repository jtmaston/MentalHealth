function load_message(id) {
    var to_be_refreshed = id.substr(id.length - 1)
    document.to_be_refreshed = to_be_refreshed

    $.get('/entry_replier/' + to_be_refreshed, function(data) {
        $('#mydiv').html(data);
    });

    console.log(document.to_be_refreshed)
}
