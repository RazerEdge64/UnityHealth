var action;
var tag;
var tag_type;
var SID;
var csrf_token;
var UPDATED_SCORES = new Set()

function actionsCardsInitializeVariables(action, tag, tag_type, SID, csrf_token){
  console.log("actionsCardsInitializeVariables->", action, tag, tag_type, SID);
  action = action;
  tag = tag;
  tag_type = tag_type;
  SID = SID;
  csrf_token = csrf_token;
}

$(".nav-item").find(".train").addClass("active");
window.onscroll = function() {scrollFunction()};
    
function scrollFunction() {
  var mybutton = document.getElementById("scroll_top");
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// ----- SAVE ------
function updated_scores(pid){
    
  console.log("Hello");
  console.log(pid);;
  UPDATED_SCORES.add(pid);
  console.log(UPDATED_SCORES);
}

function save_values(){
    $("#SpiningLoader").removeAttr('hidden');
    console.log("save_values()->", action, tag, tag_type, SID);
    // alert("save_values() -> ", action, tag, tag_type, SID);
      
      var form = document.getElementById("#form_tag_update");
      var big_list = [];
      var small_list = [];
      var prod_list = [];
      var tags_list = [];
      var prod_id = document.getElementsByName('prod_id[]');
      var tags = document.getElementsByName('tag_rel[]');

      var length = tags.length;

      for(i=0;i<length;i++){
          var temp=[];
          // if( tags[i].value==='' || tags[i].value==="-1" || tags[i].value== "-1.0" || tags[i].value== "nan" ){
          //     continue;
          // }
          if( tags[i].value==='' || tags[i].value== "nan" || tags[i].value>100 || tags[i].value<-1){
            console.log('condition failed')
            continue;
          }
          prod_list.push(prod_id[i].value);
          tags_list.push(tags[i].value);
          temp.push(prod_id[i].value);
          temp.push(tags[i].value);
          big_list.push(temp);
      }
      // alert(big_list);
      // alert(UPDATED_SCORES);
      //console.log("BIG-LIST--> ",big_list)
      //console.log("PROD - >",prod_list);
      //console.log("TAGS - >",tags_list);
      //console.log("Length--> ",length)
      //console.log("Prod-ID--> ", prod_id);
      //console.log("Tags--> ", tags);
      
      // $.ajax({
      //   type:'POST',
      //   url:'/VE_CardsSave/',
      //   data:
      //   {
      //     csrfmiddlewaretoken: csrf_token,
      //     dummy_tag_name : tag,
      //     dummy_tag_type : tag_type,
      //     dummy_prod_id : prod_list,
      //     dummy_session_number : SID,
      //     dummy_tags : tags_list
      //   },
      //   success: function(data){
      //     // alert(data);
      //   },
      //   error: function(){
      //     console.log("error while saving");
      //   }
      // });
      _updated_scores = Array.from(UPDATED_SCORES);
      console.log(_updated_scores);
      // if(prod_list.length>0){
      if( _updated_scores.length>0 ){
          document.getElementById("dummy_prod_id").value = prod_list;
          document.getElementById("dummy_updated_prod_id").value = Array.from(UPDATED_SCORES);
          document.getElementById("dummy_tags").value = tags_list;
          document.getElementById("dummy_form").submit();
      }
      else{
        alert("Nothing to save!");
        $("#SpiningLoader").attr('hidden',true);
      }

  }

  //---Save ITRN---
  function save_values_itrn(){
    console.log("save values itrn");
    $("#SpiningLoader").removeAttr('hidden');
    console.log("Clicked Save itrn");
      

      var big_list = [];
      var small_list = [];
      var prod_list = [];
      var tags_list = [];
      var prod_id = document.getElementsByName('prod_id_itrn[]');
      var tags = document.getElementsByName('tag_rel_itrn[]');

      var length = tags.length;
      console.log("Tags length - ", length)
      for(i=0;i<length;i++){
          var temp=[];
          // if( tags[i].value==='' || tags[i].value==="-1" || tags[i].value== "-1.0" || tags[i].value== "nan" ){
          //     //console.log("empty");
          //     continue;
          // }
          if( tags[i].value==='' || tags[i].value== "nan" || tags[i].value>100 || tags[i].value<-1){
            alert('Wrong score provided for a product!')
            continue;
          }          
          prod_list.push(prod_id[i].value);
          tags_list.push(tags[i].value);
          temp.push(prod_id[i].value);
          temp.push(tags[i].value);
          big_list.push(temp);
      }
      //alert(big_list);
      //console.log("BIG-LIST--> ",big_list)
      // console.log("PROD - >",prod_list);
      // console.log("TAGS - >",tags_list);
      //console.log("Length--> ",length)
      //console.log("Prod-ID--> ", prod_id);
      //console.log("Tags--> ", tags);
      _updated_scores = Array.from(UPDATED_SCORES);
      console.log(_updated_scores);      
      // if(prod_list.length>0){
      if(_updated_scores.length>0){
        document.getElementById("dummy_prod_id_itrn").value = prod_list;
        document.getElementById("dummy_updated_prod_id_itrn").value = Array.from(UPDATED_SCORES);
        document.getElementById("dummy_tags_itrn").value = tags_list;
        console.log("Submitting Form");
        document.getElementById("dummy_form_itrn").submit();
    }
    else{
      alert("Nothing to save!");
      $("#SpiningLoader").attr('hidden',true);
    }
  }

  // --- FINALIZE ---
  function finalize_values(){
      
      //document.getElementById("finalize_form").submit();
      // console.log("finalised")
      console.log("His")
      $.ajax({
        type: 'POST',
        url:'/check_saved_products',
        
        data:{
          csrfmiddlewaretoken: csrf_token,
          SID : SID,
          tag : tag,
          action : action
        },
        success : function(data){
          var x = data.data
          var y = data.unsaved_prods
          var saved_prods = (x!=null) ? parseInt(x):0
          var unsaved_prods = (y!=null) ? parseInt(y):0
          console.log("Unsaved-",unsaved_prods)
          console.log("saved-",saved_prods);
          if(saved_prods>=500){
            $("#SpiningLoader").removeAttr('hidden');  
            document.getElementById("finalize_form").submit();
          }
          else{
            $("#save_more_prods").modal('toggle');
            $("#no_of_saved_prods").text(saved_prods);
            $("#ConfirmFinalize").modal('toggle');
          }
        }
      });
            
  }

  // --- FINALIZE ---
  function finalize_values_itrn(){

    $.ajax({
      type: 'POST',
      url:'/check_saved_products',
      
      data:{
        csrfmiddlewaretoken: csrf_token,
        SID : SID,
        tag : tag,
        action : action
      },
      success : function(data){
        var x = data.data
        var y = data.unsaved_prods
        console.log(y)
        var saved_prods = (x!=null) ? parseInt(x):0
        var unsaved_prods = (y!=null) ? parseInt(y):0
        //console.log(saved_prods);
        console.log("Unsaved-",unsaved_prods)
        console.log("saved-",saved_prods);        
        if(saved_prods>=500 || unsaved_prods<=500){
          $("#SpiningLoader").removeAttr('hidden');   
          document.getElementById("finalize_form_itrn").submit();
        }
        else{
          $("#save_more_prods").modal('toggle');
          $("#no_of_saved_prods").text(saved_prods);
          $("#ConfirmFinalize_ITRN").modal('toggle');
        }
      }
    });

    
         
  }


