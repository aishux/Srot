function filter(input) {
    var filter = $(input).val().toLowerCase();
    
    var $th = $(input).closest('th');
    console.log($th)
    var col = $th.parent().children("th").index($th)-1;

    $("#data-table > tbody > tr").filter(function () {
       $(this).toggle($(this).find("td").eq(col).text().toLowerCase().indexOf(filter) > -1);
    });
}
