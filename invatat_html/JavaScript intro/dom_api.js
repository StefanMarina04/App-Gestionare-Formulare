// selectare
let sign = document.getElementById("DivSign");
console.log(sign);

let initialContent = sign.innerHTML;
let initialColor = sign.style.color;

function changeText(){
// modificare 
sign.textContent = "You are welcome :) !";
sign.innerHTML = sign.innerHTML + "<p>Hello!</p>"

// schimbare stilizare

sign.style.color = "blue";
}

function resetText()
{
    sign.innerHTML = initialContent;
    sign.style.color = initialColor;
}

let button = document.getElementById("ChangeButton");

let toggled = false;

button.onclick = function () {
    if (!toggled) {
        changeText();
    } else {
        resetText();
    }
    toggled = !toggled;
};