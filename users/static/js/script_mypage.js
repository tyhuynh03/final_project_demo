function showLibrary() {
    var libraryItems = document.getElementById("libraryItems");
    if (libraryItems.style.display === "none") {
        libraryItems.style.display = "block";
    } else {
        libraryItems.style.display = "none";
    }
}
function logout() {
    var form = document.getElementById('logout-form');
    form.submit();
}
<<<<<<< HEAD
<<<<<<< HEAD


document.addEventListener("DOMContentLoaded", function () {
=======
document.addEventListener("DOMContentLoaded", function() {
>>>>>>> 6ffb5672b476ad0d0ed13b274c059e3012d1c855
=======
document.addEventListener("DOMContentLoaded", function() {
>>>>>>> 6ffb5672b476ad0d0ed13b274c059e3012d1c855
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    const boxWrapper = document.querySelector(".box-wrapper");
    const boxWidth = document.querySelector(".box").offsetWidth;
    let scrollAmount = 0;

<<<<<<< HEAD
<<<<<<< HEAD
    nextBtn.addEventListener("click", function () {
=======
    nextBtn.addEventListener("click", function() {
>>>>>>> 6ffb5672b476ad0d0ed13b274c059e3012d1c855
=======
    nextBtn.addEventListener("click", function() {
>>>>>>> 6ffb5672b476ad0d0ed13b274c059e3012d1c855
        scrollAmount += boxWidth + 20; // 20px là khoảng cách giữa các box
        boxWrapper.style.transform = `translateX(-${scrollAmount}px)`;
    });

<<<<<<< HEAD
<<<<<<< HEAD
    prevBtn.addEventListener("click", function () {
=======
    prevBtn.addEventListener("click", function() {
>>>>>>> 6ffb5672b476ad0d0ed13b274c059e3012d1c855
=======
    prevBtn.addEventListener("click", function() {
>>>>>>> 6ffb5672b476ad0d0ed13b274c059e3012d1c855
        scrollAmount -= boxWidth + 20; // 20px là khoảng cách giữa các box
        if (scrollAmount < 0) scrollAmount = 0;
        boxWrapper.style.transform = `translateX(-${scrollAmount}px)`;
    });
});
