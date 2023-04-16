
function loadHelper(data){
    // console.log("LOAD HELPER - - ", data);
    if(data.tab){
        var tab = data.tab;

        if(tab=="new-products-tab"){
            $('#cardsTemplate').tmpl(data).appendTo("#new_product_cards"); 
        }
        else if(tab=="predicted-tab"){
            $('#cardsTemplate').tmpl(data).appendTo("#predicted_product_cards");
        }
        else if(tab=="trained-tab"){
            $('#cardsTemplate').tmpl(data).appendTo("#trained_product_cards");
        }
    } else{
        $('#cardsTemplate').tmpl(data).appendTo("#product_cards");
    }
    // feather.replace();
}
