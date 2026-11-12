function hidePre(){var p=document.getElementById("pre");if(p)p.style.display="none"}
addEventListener("load",hidePre);setTimeout(hidePre,2500);
var y=document.getElementById("yr");if(y)y.textContent=new Date().getFullYear();
var T=[].slice.call(document.querySelectorAll(".tab"));
T.forEach(function(t){t.addEventListener("click",function(){T.forEach(function(x){var on=x===t;x.setAttribute("aria-selected",on);document.getElementById("pn"+x.dataset.i).hidden=!on})})});
function calc(){var a=+r1.value,b=+r2.value,c=+r3.value,d=+r4.value;o1.textContent=a;o2.textContent=b;o3.textContent=c;o4.textContent=d;var t=a*b*c*52;v1.textContent="\u20b9"+t.toLocaleString("en-IN");v2.textContent="\u20b9"+Math.round(t*d/100).toLocaleString("en-IN")}
if(window.r1){[r1,r2,r3,r4].forEach(function(e){e.addEventListener("input",calc)});calc()}