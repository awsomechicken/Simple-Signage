
function deleteContent(cid, csrf){
  var yes_delete = confirm("Delete Content: #"+cid+"?\n");
  if (yes_delete) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/deletecontent", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("csrfmiddlewaretoken="+csrf+"&Delete="+cid);
    location.reload(true); // reload the page
  }
}


function tsv(el_id){
  // toggle_settings_visability
  var x = document.getElementById(el_id);
  if (x.style.display === "none") {
    x.style.display = "block";
  }
  else {
    x.style.display = "none";
  }
}

function picture_preview(file_path){
  // from: https://www.muicss.com/docs/v1/css-js/overlay
  // part of the material-ui (mui) js+css package
  // initialize modal element
  var modalEl = document.createElement('div');
  modalEl.style.width = '80%';
  //modalEl.style.height = '300px';
  modalEl.style.margin = '2.5% auto';
  modalEl.style.top = '8em';

  if(file_path.search(".mp4") > 0){
    // search("...") > 0 is equivelant to .contains("...")
    // need to add a video tag for videos
    modalEl.innerHTML = "<div align=\"center\"><video src="+file_path+" width=\"100%\" autoplay loop></video>";
  }
  else{
    modalEl.innerHTML = "<div align=\"center\"><img src="+file_path+" width=\"100%\"></div>";
  }


  // show modal
  mui.overlay('on', modalEl);
}

function submitContentChanges(){
  // for detached submit button to submit the changes
  //var content_form = document.getElementById("contentChangeForm")//.submit()
  var content_form = $("#contentChangeForm");
  console.log(content_form);

  var http = new XMLHttpRequest();
    http.open("POST", "apply_changes", true);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    //var params = "search=" + <<get search value>>; // probably use document.getElementById(...).value
    //var params = content_form.seralize();
    //console.log(params);
    /*http.send(params);
    http.onload = function() {
        alert(http.responseText);
    }*/
}
