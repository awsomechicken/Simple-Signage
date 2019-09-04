// update the time every second
var v = setInterval(tu,1000);

function tu(eid){
  var da = new Date();
  document.getElementById("updateMe").innerHTML = da.toLocaleString();
  //console.log("")
}
