
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
  modalEl.style.width = '60%';
  //modalEl.style.height = '300px';
  modalEl.style.margin = '2.5% auto';
  modalEl.style.top = '8em';

  if(file_path.search(".mp4") > 0){
    // search("...") > 0 is equivelant to .contains("...")
    // need to add a video tag for videos
    modalEl.innerHTML = "<div align=\"center\"><video src="+file_path+" width=\"auto\" height = \"auto\" autoplay loop></video>";
  }
  else{
    modalEl.innerHTML = "<div align=\"center\"><img src="+file_path+" width=\"100%\" height = \"auto\"></div>";
  }

  // show modal
  mui.overlay('on', modalEl);
}

function submitContentChanges(){
  // for detached submit button to submit the changes
  var ccf = document.getElementById("contentChangeForm");
  ccf.submit();
}

var checkingForVideo; // global for controlling the overlay

function compileVideo(csrf){
  sendMakeVideo(csrf); // sent the command to make the video
  deactivate_compbtn(); // deactivate the button
  video_compiling_overlay();
  setTimeout(function () {
    checkingForVideo = setInterval(function(){checkForVideoDone(csrf);},1000);
  }, 800);
}

function deactivate_compbtn(){
  // disable the compile button to avoid confusion...
  document.getElementById('compileVideo').disabled = true;
}

function video_compiling_overlay(){
  var loading_overlay = document.createElement('div');
  loading_overlay.id = "Modal Overlay";
  //loading_overlay.style.width = '30%';
  //loading_overlay.style.height = '100%'
  //loading_overlay.style.margin = '2.5% auto';
  //loading_overlay.style.top = '15%';
  //loading_overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
  //loading_overlay.style.zIndex = '2';
  loading_overlay.innerHTML = "<div class=\"modal\"><div class=\"modal-content\"><img src=\"/static/cat_loading.gif\"><p>Please be patient as we are doing things...<p><p id=\"funnies\"><p></div></div>";
  //loading_overlay.innerHTML = "<img src=\"/static/cat_loading.gif\">"
  //loading_overlay.style.display = "block";
  mui.overlay('on', loading_overlay)
  // show message saying to be patient because it could take a while, and gray-out the compile_video button
}

function sendMakeVideo(csrf){
  // Send post to server to initiate the process
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/makevideo", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("csrfmiddlewaretoken="+csrf);
}

function checkForVideoDone(csrf){
  var xhttp = new XMLHttpRequest();
  xhttp.open("get", "/video_compile_status_request", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function() { // response update stuff
    if (this.readyState == 4 && this.status == 200) {
      //document.getElementById("funnies").innerHTML = this.responseText;

      if(this.responseText == "False"){
        clearInterval(checkingForVideo) // stop polling the server for stuff
        document.getElementById("Modal Overlay").remove(); // remove the overlay
        document.getElementById('compileVideo').disabled = false; // reactivate the compile button
      }
    }
  };
  xhttp.send("csrfmiddlewaretoken="+csrf);
}

// check if there is a video compiling on the server before trying anything
function isServerCompilingVideo(csrf){
  console.log("Checking for video compiling");
  var xhttp = new XMLHttpRequest();
  xhttp.open("get", "/video_compile_status_request", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function() { // response update stuff
    if (this.readyState == 4 && this.status == 200) {
      if(this.responseText == "False"){
        console.log("no video compiling");
      }
      if(this.responseText == "True"){
        console.log("Video is currently compiling, enabling cat");
        deactivate_compbtn(); // deactivate the button
        video_compiling_overlay();
        setTimeout(function () {
          checkingForVideo = setInterval(function(){checkForVideoDone(csrf);},1000);
        }, 800);
      }
    }
  };
  xhttp.send("csrfmiddlewaretoken="+csrf);
}
