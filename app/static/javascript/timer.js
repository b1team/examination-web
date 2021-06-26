var today = new Date();
var ttt = parseInt(document.getElementById("time-left").value);
var tt = 600;
var time = today.getTime();
$(document).ready(function () {
    var ttt = parseInt(document.getElementById("time-left").value);
    showTime();
});

function showTime() { 
    var today = new Date(); 
    var t = ttt- Math.floor((today.getTime() - time) / 1000);
    if (t <= 0) { 
        location.href = '/timeout'; 
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
        document.getElementById('timer').innerHTML = str; 
        setTimeout("showTime()", 1000); 
    } 
}