
function addScreen(){
  //alert("THings");

  var x = document.getElementById("addScreenPlace");
  if (x.style.display === "none") {
    x.style.display = "block";
    document.getElementById("addScreenBtn").disabled = true;
  }
  /*else {
    x.style.display = "none";
  }*/
  //document.getElementById("addScreenPlace").innerHTML = "Pressed!";
}

function addScreenField(){
  // append a feild to the add form.
  console.log("15: addScreenField()")
}
