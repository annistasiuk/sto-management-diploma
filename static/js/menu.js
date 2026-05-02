const burger = document.getElementById("burger");
const menu = document.getElementById("menu");
const close = document.getElementById("close");
const links = document.querySelectorAll(".nav-item");

burger.addEventListener("click", function(){
    menu.classList.toggle("active");
    document.body.classList.toggle("no-scroll");
});

close.addEventListener("click", function(){
    menu.classList.remove("active");
    document.body.classList.remove("no-scroll");
});

links.forEach(link => {
    link.addEventListener("click", () => {
        menu.classList.remove("active");
        document.body.classList.remove("no-scroll");
    });
});