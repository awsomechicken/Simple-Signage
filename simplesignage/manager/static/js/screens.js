function addScreen(){
  //alert("THings");

  var x = document.getElementById("addScreenPlace");
  if (x.style.display === "none") {
    x.style.display = "block";
    document.getElementById("addScreenBtn").disabled = true;
  }
  else {
    x.style.display = "none";
    document.getElementById("addScreenBtn").disabled = false;
  }
  //document.getElementById("addScreenPlace").innerHTML = "Pressed!";
}

function addScreenSubmit(){
  // submit the stuff, with verification
  console.log("15: addScreenField()")
}

function deleteScreenConfirm(screen_id, csrf){
  var yesno = confirm("Delete Screen: "+screen_id+"?");
  if(yesno){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/deletescreen", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("csrfmiddlewaretoken="+csrf+"&Delete="+screen_id);
    location.reload(true); // reload the page
  }
}

function addScreenVerify(){
  // verify the settings for the newest screen
  console.log("Stuff N' Things");
}
