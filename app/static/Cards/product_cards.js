//import test from 'card_variables';
// console.log(test);

var tag;
var tag_type;
var SID;
var action;
var search_val;
var csrf_token;
var sort_name = 1;
var sort_relevancy = 0;
var sort_date = -1; // Desc

var tab="new-products-tab";

var page = 0;
var pageLimit = 1;
var limit = 1000;
var offset = 0;
var TOTAL_PRODUCTS = 0;
var ALL_PRODUCTS_LENGTH = 0;
var ALL_PRED_PRODS = 0;
var ALL_TRAINED_PRODS = 0;
var NEW_PRODUCTS_LENGTH = 0;

// var UPDATED_SCORES = new Set()
// --- Functions ---

function initializeVariables(tag, tag_type, SID, action, search_val, csrf_token){
    tag = tag;
    tag_type = tag_type;
    SID = SID;
    action = action;
    search_val = search_val;
    csrf_token = csrf_token;
    console.log("Variables Initialized");
}

function fetchSessionDetails(){
    $.ajax({
        type : 'GET',
        url : '/fetch_session_details?SID='+SID,
        success : function(data){
            //console.log(data);
            session = data['SESSION']
            SID = session['SID']
            // console.log("Session ID",SID)
            console.log("Fetching Session Details...")
            $("#ITR_NO").text(" ITR - "+session['ITR_NO'])
        }
    });
}

// -- Load Products --
function loadProducts(offset, limit, search_val){
    $("#SpiningLoader").removeAttr('hidden');

    $("#product_cards").empty();
    $("#new_product_cards").empty();
    $("#predicted_product_cards").empty();
    $("#trained_product_cards").empty();

    // var sort_name = $("#sort_name").attr("data-sort");

    console.log("offset->",offset, "| limit->",limit, "|--| Tag->",tag, "| action->",action, "| SID->",SID, "| SearchVal->",search_val, " | Tab->",tab," | SortName->",sort_name, " | Sort Rel->",sort_relevancy, " | Page->",page);

    // AJAX
    $.ajax({
        type: 'POST',
        url: "/products_card",
        data:
        {
        csrfmiddlewaretoken: csrf_token,
        search : search_val,
        tag : tag,
        SID : SID,
        action : action,
        offset : offset,
        limit : limit,
        sort_name : sort_name,
        sort_relevancy:sort_relevancy,
        sort_date : sort_date,
        tab:tab,
        search_type:$("#searchType").val()
        },
        success: function(data){
            ALL_PRODUCTS_LENGTH = data['ALL_PRODUCTS_LENGTH'];
            if(action=="view" || action=="edit"){
                ViewEdit(data);
            }
            else if(action=="train_more"){
                console.log("train_more");
                TrainMore(data);
            }

            lazy();
        }

    });
}

function ViewEdit(data){
    console.log("ViewEdit");
    console.log(" > Data-",data)
    var product_json = JSON.parse(data['PRODUCTS']);    // Fetching Products

    TOTAL_PRODUCTS = data['TOTAL_PRODUCTS_INT']
    set_total_products(TOTAL_PRODUCTS);     // Function

    pageLimit = Math.ceil(TOTAL_PRODUCTS/limit);   // Calculating pageLimit
    set_pagination_details(page+1, pageLimit);    // Function

    var static_file = "'/static/images/snake-plant.png'"
    var final_list=[] ;
    $.each(product_json, function(index, data){
        var product_type_tags = data.PRODUCT_TYPE_TAGS;

        var ptt_body = get_ptt(product_type_tags);  // PTT Function

        var product_description = JSON.stringify(data.PRODUCT_DESCRIPTION);
        //var CRSF = '{{ csrf_token }}'
        var PID = "'"+data.PRODUCT_DIMENSION_ID+"'";
        var input_field;
        var card_theme;
        var table_theme;

        if(data.USER_SCORE>0){
            card_theme = '<div class="card border-success" style="width:20rem ; margin:10px ; background-color:#fbfffc">';
            table_theme = '<tr class="table-success">';

        }else if(data.USER_SCORE==0){
            card_theme = '<div class="card" style="width:20rem ; margin:10px">';
            table_theme = '<tr class="table-success">';
        }else{
            card_theme = '<div class="card border-secondary" style="width:20rem ; margin:10px; background-color:#f0f0f0">';
            table_theme = '<tr class="table-secondary">';    
        }


        if(action=='view'){
            input_field = '<th scope="col" style="text-align: center;">'+tag_type+' TAG</th>\
            <th scope="col" style="text-align: center;" >Your Score</th>\
            </tr>\
        </thead>\
        <tbody>\
            <tr>\
                <td style="text-align: center;">\
                    <div class="badge bg-success" style="vertical-align: -webkit-baseline-middle;">\
                        <text style="font-size: 14px;">'+tag+'</text>\
                    </div>\
                </td>\
                <td style="text-align: center;">\
                    <div class="input-group input-group-sm mb-3" >\
                        <input name="prod_id[]"  value='+data.PRODUCT_DIMENSION_ID+' type="text" class="form-control" hidden>\
                        <input readonly name="tag_rel[]"  value='+data.USER_SCORE+' style=" border-radius:10%" type="text" class="form-control">\
                    </div>\
                </td>\
            </tr>\
        </tbody>';
        }
        else{
            input_field = '<th scope="col" style="text-align: center;">'+tag_type+' TAG</th>\
            <th scope="col" style="text-align: center;" >Your Score</th>\
            </tr>\
        </thead>\
        <tbody>\
            <tr>\
                <td style="text-align: center;">\
                    <div class="badge bg-success" style="vertical-align: -webkit-baseline-middle;">\
                        <text style="font-size: 14px;">'+tag+'</text>\
                    </div>\
                </td>\
                <td style="text-align: center;">\
                    <div class="input-group input-group-sm mb-3" >\
                        <input name="prod_id[]"  value='+data.PRODUCT_DIMENSION_ID+' type="text" class="form-control" hidden>\
                        <input name="tag_rel[]"  type="number" min="0" max="100" value='+data.USER_SCORE+' onblur="updated_scores('+PID+');" style=" border-radius:10%" class="form-control">\
                    </div>\
                </td>\
            </tr>\
        </tbody>';
        }
        data.card_theme = card_theme;
        data.table_theme = table_theme; 
        data.input_field = input_field
        data.ptt_body = ptt_body
        data.TAG=tag;
        // data.TAG_TYPE=tag_type;
        data.description_parse = JSON.parse(product_description)
        data.product_description = product_description;
        
        if (data.SCORE_UPDATED==""){
            data.score_updated = "Not saved yet."
        }
        else{
            var date_time_timestamp = new Date(data.SCORE_UPDATED);
            data.score_updated = date_time_timestamp.toLocaleDateString()+" , "+date_time_timestamp.toLocaleTimeString();
        }
        
        // ---
        loadHelper(data);
        // $("#product_cards").append(html);
        // final_list.push(data);
        $("#SpiningLoader").attr('hidden', true)
    });
}

function TrainMore(data){

    console.log("TrainMore ", tab);
    //console.log(data);
    if(tab=="new-products-tab"){
        TOTAL_PRODUCTS = data['NEW_PRODUCTS_LENGTH']
        var product_json = JSON.parse(data['PRODUCTS']);
        console.log('new-products-tab')
    }
    else if(tab=="predicted-tab"){
        TOTAL_PRODUCTS = data['PREDICTED_LENGTH']
        var product_json = JSON.parse(data['PREDICTED']);
        console.log("predicted_tab ",TOTAL_PRODUCTS);
    }
    else if(tab=="trained-tab"){
        TOTAL_PRODUCTS = data['TRAINED_LENGTH']
        var product_json = JSON.parse(data['TRAINED']);
        console.log("trained_tab ",TOTAL_PRODUCTS);
    }

    set_total_products(TOTAL_PRODUCTS);     // Function

    pageLimit = Math.ceil(TOTAL_PRODUCTS/limit);   // Calculating pageLimit
    set_pagination_details(page+1, pageLimit);    // Function

    var static_file = "'/static/images/snake-plant.png'"

    $.each(product_json, function(index, data){
        //console.log(data);
        var product_type_tags = data.PRODUCT_TYPE_TAGS;
        var relevancy_area = '';
        //console.log(data,product_type_tags);
        //console.log(product_type_tags.length);
        var PID = "'"+data.PRODUCT_DIMENSION_ID+"'";
        if(tab=="new-products-tab"){
            relevancy_area = '<th scope="col" style="text-align: center;">'+tag_type+' TAG</th>\
            <th scope="col" style="text-align: center;" >Your Score</th>\
            </tr>\
            </thead>\
            <tbody>\
                <tr>\
                    <td style="text-align: center;">\
                        <div class="badge bg-success" style="vertical-align: -webkit-baseline-middle;">\
                            <text style="font-size: 14px;">'+tag+'</text>\
                        </div>\
                    </td>\
                    <td style="text-align: center;">\
                        <div class="input-group input-group-sm mb-3" >\
                            <input name="prod_id_itrn[]"  value='+data.PRODUCT_DIMENSION_ID+' type="text" class="form-control" hidden>\
                            <input name="tag_rel_itrn[]"  value='+data.USER_SCORE+' onblur="updated_scores('+PID+');" style=" border-radius:10%" type="number" min="0" max="100" class="form-control">\
                        </div>\
                    </td>\
                </tr>\
            </tbody>\
            ';
        }
        else if(tab=="predicted-tab"){
            relevancy_area = '<th scope="col" style="text-align: center;">'+tag_type+' TAG</th>\
            <th scope="col" style="text-align: center;" >Your Score</th>\
            <th scope="col" style="text-align: center;" >PRED</th>\
            </tr>\
            </thead>\
            <tbody>\
            <tr>\
                <td style="text-align: center;">\
                    <div class="badge bg-success" style="vertical-align: -webkit-baseline-middle;">\
                        <text style="font-size: 14px;">'+tag+'</text>\
                    </div>\
                </td>\
                <td style="text-align: center;">\
                    <div class="input-group input-group-sm mb-3" >\
                        <input name="tag_rel[]" readonly value='+data.USER_SCORE+' style=" border-radius:10%" type="text" class="form-control">\
                    </div>\
                </td>\
                <td style="text-align: center;">\
                    <div class="input-group input-group-sm mb-3" >\
                        <input name="tag_pred_rel[]" readonly value='+data.PREDICTED_SCORE+' style=" border-radius:10%" type="text" class="form-control">\
                    </div>\
                </td>\
            </tr>\
            </tbody>\
            ';
        }
        else if(tab=="trained-tab"){
            relevancy_area = '<th scope="col" style="text-align: center;">'+tag_type+' TAG</th>\
            <th scope="col" style="text-align: center;" >Your Score</th>\
            </tr>\
            </thead>\
            <tbody>\
                <tr>\
                    <td style="text-align: center;">\
                        <div class="badge bg-success" style="vertical-align: -webkit-baseline-middle;">\
                            <text style="font-size: 14px;">'+tag+'</text>\
                        </div>\
                    </td>\
                    <td style="text-align: center;">\
                        <div class="input-group input-group-sm mb-3" >\
                            <input name="prod_id[]" readonly value='+data.PRODUCT_DIMENSION_ID+' type="text" class="form-control" hidden>\
                            <input name="tag_rel[]" readonly value='+data.USER_SCORE+' style=" border-radius:10%" type="text" class="form-control">\
                        </div>\
                    </td>\
                </tr>\
            </tbody>\
            ';
        }
        var ptt_body = get_ptt(product_type_tags);  // PTT Function
        var product_description = JSON.stringify(data.PRODUCT_DESCRIPTION);
        var input_field;
        var card_theme;
        var table_theme;

        if(data.USER_SCORE>0 || data.PREDICTED_SCORE){
            card_theme = '<div class="card border-success" style="width:20rem ; margin:10px ; background-color:#fbfffc">';
            table_theme = '<tr class="table-success">';    
            }
        else if(data.USER_SCORE==0){
            card_theme = '<div class="card" style="width:20rem ; margin:10px">';
            table_theme = '<tr class="table-success">';
            }
        else{
            card_theme = '<div class="card border-secondary" style="width:20rem ; margin:10px; background-color:#f0f0f0">';
            table_theme = '<tr class="table-secondary">';    
            }

        data.card_theme = card_theme;
        data.table_theme = table_theme; 
        data.input_field = relevancy_area
        data.ptt_body = ptt_body
        data.TAG=tag;
        // data.TAG_TYPE=tag_type;
        data.description_parse = JSON.parse(product_description);
        data.tab = tab;
        data.product_description = product_description;
        var date_time_timestamp = new Date(data.SCORE_UPDATED)
        if (data.SCORE_UPDATED==""){
            data.score_updated = "Not saved yet."
        }
        else{
            var date_time_timestamp = new Date(data.SCORE_UPDATED);
            data.score_updated = date_time_timestamp.toLocaleDateString()+" , "+date_time_timestamp.toLocaleTimeString();
        }
        //
        loadHelper(data);

        // if(tab=="new-products-tab"){
        //     $("#new_product_cards").append(html);    
        // }
        // else if(tab=="predicted-tab"){
        //     $("#predicted_product_cards").append(html);
        // }
        // else if(tab=="trained-tab"){
        //     $("#trained_product_cards").append(html);
        // }
        
    });
    $("#SpiningLoader").attr('hidden', true)
}
// --------------------------
function get_ptt(ptt_array){
    var final_str = ''
    if(ptt_array.length>0){
        for(i=0;i<ptt_array.length;i++){
            var name = ptt_array[i][0]
            var score = ptt_array[i][1]
            if(score==null || name==null){
                score = "-";
                name = "-"
                var html = '<tr>\
                    <td style="text-align: center;">'+name+'</td>\
                    <td style="text-align: center;">'+score+'</td>\
                </tr>'
            }
            else{
                var html = '<tr>\
                            <td>'+name+'</td>\
                            <td style="text-align: center;">'+score+'</td>\
                        </tr>'
            }
            final_str = final_str+html            
        }
        
    }
    return final_str
}
// --
function set_total_products(TOTAL_PRODUCTS){
    // console.log("<<set_total_products>>", TOTAL_PRODUCTS);
    if(action=="view" || action=="edit"){
        if((page+1)*limit > TOTAL_PRODUCTS){
            $("#no_of_products").text("Showing "+TOTAL_PRODUCTS+" of "+TOTAL_PRODUCTS+" products.")    
        }
        else{
            $("#no_of_products").text("Showing "+(page+1) * (limit)+" of "+TOTAL_PRODUCTS+" products.")
        }
    }
    else{
        if((page+1)*limit > TOTAL_PRODUCTS){
            $(".no_of_products").text("Showing "+TOTAL_PRODUCTS+" of "+TOTAL_PRODUCTS+" products.")    
        }
        else{
            $(".no_of_products").text("Showing "+(page+1) * (limit)+" of "+TOTAL_PRODUCTS+" products.")
        }
    }
}

function set_pagination_details(page, pageLimit){
    if(action=="view" || action=="edit"){
    $("#pagination_details").text(page+" of "+pageLimit)
    }
    else{
        $(".pagination_details").text(page+" of "+pageLimit)
    }
}


//------ Searching ------
function searchProds(){
    offset=0;
    page = 0;
    //
    $("#go_to_page").val("");
    $("#go_to_page_new_prods").val("");
    $("#go_to_page_pred_prods").val("");
    $("#go_to_page_trained_prods").val("");

    //
    if(action=="view" || action=="edit"){
        
        search_val = document.getElementById("search_prods_id").value
        console.log("Search clicked..",search_val, action);

        loadProducts(offset, limit, search_val);
    }
    else{
        if(tab=="new-products-tab"){
            search_val = document.getElementById("search_new_prods_id").value;

        }
        else if(tab=="predicted-tab"){
            search_val = document.getElementById("search_pred_prods_id").value;

        }
        else if(tab=="trained-tab"){
            search_val = document.getElementById("search_trained_prods_id").value;

        }

        console.log("Search clicked..",search_val, action, tab);
        loadProducts(offset, limit, search_val);
    }
    
}
// ------- Sorting -------
$(".sort_name").on("click",function(){
    // 1 - > ascending - arrow-down;    
    // -1 -> descending - arrow-up;
    console.log('sort_name clicked', sort_name);
    sort_date = 0;
    sort_relevancy=0;

    if(action=="view" || action=="edit"){

        if(sort_name==1){
            $("#span_sort_name").attr("data-feather","arrow-down");
            feather.replace()
            page=0;
            // $("#sort_name").attr("data-sort",-1);
            sort_name=-1;
            loadProducts(offset, limit, search_val) // Loading Products
            
        }
        else{
            $("#span_sort_name").attr("data-feather","arrow-up");
            feather.replace()
            page=0;
            // $("#sort_name").attr("data-sort",1);
            sort_name=1;
            loadProducts(offset, limit, search_val) // Loading Products
            
        }
    }
    else{
        //

        if(tab=="new-products-tab"){
            //var data_sort = $("#sort_name").attr("data-sort");
            //console.log(tag," Sort Name",data_sort);
            if(sort_name==1){
                $("#span_sort_name").attr("data-feather","arrow-down");
                feather.replace()
                page=0;
                //$("#sort_name").attr("data-sort",-1);
                sort_name=-1;
                loadProducts(offset, limit, search_val) // Loading Products
                
            }
            else{
                $("#span_sort_name").attr("data-feather","arrow-up");
                feather.replace()
                page=0;
                //$("#sort_name").attr("data-sort",1);
                sort_name=1;
                loadProducts(offset, limit, search_val) // Loading Products
                
            }
        }
        else if(tab=="predicted-tab"){

            //var data_sort = $("#sort_name_predicted").attr("data-sort");
            console.log(tag," Sort Name",sort_name);
            if(sort_name==1){
                $("#span_sort_name_predicted").attr("data-feather","arrow-down");
                feather.replace()
                page=0;
                sort_name=-1;
                //$("#sort_name_predicted").attr("data-sort",-1);
                loadProducts(offset, limit, search_val) // Loading Products
                
            }
            else{
                $("#span_sort_name_predicted").attr("data-feather","arrow-up");
                feather.replace()
                page=0;
                sort_name=1;
                //$("#sort_name_predicted").attr("data-sort",1);
                loadProducts(offset, limit, search_val) // Loading Products
                
            }
        }
        else{

            //var data_sort = $("#sort_name_trained").attr("data-sort");
            console.log(tag," Sort Name",sort_name);
            if(sort_name==1){
                $("#span_sort_name_trained").attr("data-feather","arrow-down");
                feather.replace()
                page=0;
                sort_name=-1
                //$("#sort_name_trained").attr("data-sort",-1);
                loadProducts(offset, limit, search_val, tab) // Loading Products
                
            }
            else{
                $("#span_sort_name_trained").attr("data-feather","arrow-up");
                feather.replace()
                page=0;
                sort_name =1;
                //$("#sort_name_trained").attr("data-sort",1);
                loadProducts(offset, limit, search_val) // Loading Products
                
            }

        }
        //
    }
});

$(".sort_date").on("click",function(){
    sort_relevancy = 0;
    sort_name = 0;
    page=0;
    console.log("> sort_date")
    if(sort_date==0){
        sort_date = -1;
    }

    if(sort_date==1){
        $("#span_sort_date").attr("data-feather","arrow-down");
        feather.replace()
        sort_date = -1;
        loadProducts(offset, limit, search_val);
    } else{
        $("#span_sort_date").attr("data-feather","arrow-up");
        feather.replace()
        sort_date = 1;
        loadProducts(offset, limit, search_val);
    }
});

$("#sort_relevancy").on("click",function(){
    // 1 - > ascending - arrow-down;    
    // -1 -> descending - arrow-up;
    sort_name = 0;
    sort_date = 0;
    console.log("sort relevancy", sort_relevancy);
    //sort_relevancy =1;
    if(sort_relevancy==0){
        sort_relevancy=1;
    }
    if(sort_relevancy==1){
        $("#span_sort_relevancy").attr("data-feather","arrow-down");
        feather.replace()
        page=0;
        sort_relevancy = -1;
        //$("#sort_relevancy").attr("data-sort",-1);
        console.log(sort_relevancy);
        loadProducts(offset, limit, search_val) // Loading Products
        
    }
    else{
        $("#span_sort_relevancy").attr("data-feather","arrow-up");
        feather.replace()
        page=0;
        sort_relevancy = 1;
        //$("#sort_relevancy").attr("data-sort",1);
        console.log(sort_relevancy);
        loadProducts(offset, limit, search_val) // Loading Products
        
    }
});

// --- Page ---
$(".firstPage").on("click", function(){
    console.log("First Page");
});

$(".nextBtn").on("click", function(){
    console.log("Next - Page ",page)

    if( (page+1)*limit < TOTAL_PRODUCTS ){
        page++;
        console.log(page*limit);
        loadProducts(page*limit, limit, search_val)
        set_pagination_details(page+1,pageLimit)

    }

});

$(".previousBtn").on("click", function(){

    if(page>0){
        page--;
        set_pagination_details(page+1,pageLimit)
        loadProducts(page*limit, limit, search_val);
    }

});

$(".lastPage").on("click", function(){
    console.log("Last Page");
});

// -- GoTo Page --
function goToPage(){

    console.log("goto page")
    var input_page = 1;
    if(action=="view" || action=="edit"){
       input_page = document.getElementById("go_to_page").value;
    }
    else{
        if(tab=="new-products-tab"){
            input_page = document.getElementById("go_to_page_new_prods").value
        }
        else if(tab=="predicted-tab"){
            input_page = document.getElementById("go_to_page_pred_prods").value
        }
        else if(tab=="trained-tab"){
            input_page = document.getElementById("go_to_page_trained_prods").value
        }
    }
    
    console.log("GoToPage-",tab, input_page, (input_page)*limit);
    input_page = parseInt(input_page);
    if( (input_page) <= pageLimit && input_page>0){
        //offset = (input_page)*limit
        page = input_page-1;
        offset = (input_page-1)*limit
        loadProducts(offset, limit, search_val)
        
    }

}

// --------------------------- Train More Tabs ----------------------------
$("#new-products-tab").on("click", function(){
    tab = "new-products-tab";
    //search_val = $("#search_new_prods_id").text('');
    search_val='';
    page=0;
    sort_name=1;
    offset=0;
    loadProducts(offset, limit, search_val);
});
$("#predicted-tab").on("click", function(){
    tab = "predicted-tab";
    page=0;
    //search_val = $("#search_pred_prods_id").text('');
    search_val='';
    sort_name=1;
    offset=0;
    loadProducts(offset, limit, search_val);
});
$("#trained-tab").on("click", function(){
    tab = "trained-tab";
    //search_val =  $("#search_trained_prods_id").text('');
    search_val='';
    sort_name=1;
    page=0;
    offset=0;
    loadProducts(offset, limit, search_val);
});


// -- Lazy Loading --
document.addEventListener("DOMContentLoaded", function() {
    lazy();
  });

function lazy(){
    console.log("Load Lazy");
    var lazyloadImages;    

    if ("IntersectionObserver" in window) {
        lazyloadImages = document.querySelectorAll(".lazy");
        var imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
            var image = entry.target;
            image.src = image.dataset.src;
            image.classList.remove("lazy");
            imageObserver.unobserve(image);
            }
        });
        });

        lazyloadImages.forEach(function(image) {
        imageObserver.observe(image);
        });
    } else {  
        var lazyloadThrottleTimeout;
        lazyloadImages = document.querySelectorAll(".lazy");
        
        function lazyload () {
            if(lazyloadThrottleTimeout) {
                clearTimeout(lazyloadThrottleTimeout);
            }    

            lazyloadThrottleTimeout = setTimeout(function() {
                var scrollTop = window.pageYOffset;
                lazyloadImages.forEach(function(img) {
                    if(img.offsetTop < (window.innerHeight + scrollTop)) {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    }
                });
                if(lazyloadImages.length == 0) { 
                document.removeEventListener("scroll", lazyload);
                window.removeEventListener("resize", lazyload);
                window.removeEventListener("orientationChange", lazyload);
                }
            }, 20);
        }

        document.addEventListener("scroll", lazyload);
        window.addEventListener("resize", lazyload);
        window.addEventListener("orientationChange", lazyload);
    }
}

function scoreDistribution(){
    $("#score_distribution_card").removeAttr('hidden')
    $("#scores_accoridion").removeAttr('hidden')
    
    console.log("scoreDistribution");
    $.ajax({
        type : "GET",
        url : "/score_distribution?TAG="+tag+"&SID="+SID,
        success : function(data){
            console.log(data['data']);
            var distinct_scores = data['data'];
            if (distinct_scores=="NO"){
                var _total_saved = '<div class="text-center"><h6 class="text-muted"> Total saved - 0</h6></div>'
                $("#score_distribution_table").append(_total_saved)
            }
            else{
                var total_saved = data['total_saved']
                var rows = "";
                for (var key in distinct_scores) {
                    if (distinct_scores.hasOwnProperty(key)) {
                        var val = distinct_scores[key];
                        console.log(typeof(val))
                        var badge_theme = "";
                        if(val<=10){
                            badge_theme = "bg-danger";
                        }
                        else if(val>10 && val<50){
                            badge_theme = "bg-warning text-dark";
                        }
                        else if(val>=50 && val<100){
                            badge_theme = "bg-primary";
                        }
                        else if(val>=100){
                            badge_theme = "bg-success";
                        }
                        var temp = '<tr> <td style="text-align:center;"> <b>'+key+'</b></td> <td style="text-align:center;"><span class="badge '+badge_theme+' rounded-pill">'+val+'</span></td> </tr> '
                        rows = rows+temp;
                    }
                }
                var _score_table_html = '<div class="table-responsive" style="overflow:auto;max-height:300px"> <table class="table table-hover" style="width:100% ; white-space:nowrap"> <thead> <tr class="table-dark"> <th scope="col" style="text-align:center;">Scores</th> <th scope="col" style="text-align:center;">Products</th> </tr> </thead> <tbody>'+rows+'</tbody> </table> </div>';
                $("#score_distribution_table").append(_score_table_html)
    
                var _total_saved = '<div class="text-center"><h6 class="text-muted"> Total saved - <b>'+total_saved+'</b></h6></div>'
                $("#score_distribution_table").append(_total_saved)
            }

        }
    });
}