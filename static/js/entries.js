function load_message(id) {

    var to_be_refreshed = id.split('-')
    //document.vari = to_be_refreshed
    to_be_refreshed = to_be_refreshed[to_be_refreshed.length - 1]
    //console.log(to_be_refreshed)
    $.ajax({
    method:"get",
    url:"/entry_replier/" + to_be_refreshed,
    data: "",
    beforeSend:function() {},
    success:function(data){
       //console.log(html)
       $('#message-pane').html(data);
    }
    });
    return false;
}