var today = new Date();
var ttt = parseInt(document.getElementById("time-left").value);
var tt = parseInt(document.getElementById("dura").value);
var time = today.getTime();
var t = ttt- Math.floor((today.getTime() - time) / 1000);
console.log("AAAtime"+time);
$(document).ready(function () {
    var ttt = parseInt(document.getElementById("time-left").value);
    showTime();
});

function showTime() { 
    var today = new Date(); 
    var t = ttt- Math.floor((today.getTime() - time) / 1000);
    if (t <= 0) { 
        location.href = '/student'; 
    } 
    else {
        var minute = String(Math.floor(t / 60));
        var second = String(t % 60);
        if (minute.length == 1) { 
            minute = "0" + minute; 
        } 
        if (second.length == 1) { 
            second = "0" + second; 
        } 
        var str = minute + ":" + second; 
        document.getElementById('timers').innerHTML = str; 
        setTimeout("showTime()", 1000); 
    } 
}