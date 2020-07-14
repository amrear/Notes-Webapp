/* This script contains fadeOut function which makes messeges fade nice and smooth. */

function fadeOut(el){
    el.style.opacity = 1;

    (function fade() {
    if ((el.style.opacity -= .1) < 0) {
        el.style.display = "none";
    } else {
        requestAnimationFrame(fade);
    }
    })();
};
const flashedMessege = document.querySelector(".flashed-message");
if (flashedMessege != null) {
    setTimeout(function () {
        fadeOut(flashedMessege);
    }, 2000);
}