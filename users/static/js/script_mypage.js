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


document.addEventListener("DOMContentLoaded", function () {
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    const boxWrapper = document.querySelector(".box-wrapper");
    const boxWidth = document.querySelector(".box").offsetWidth;
    let scrollAmount = 0;

    nextBtn.addEventListener("click", function () {
        scrollAmount += boxWidth + 20; // 20px là khoảng cách giữa các box
        boxWrapper.style.transform = `translateX(-${scrollAmount}px)`;
    });

    prevBtn.addEventListener("click", function () {
        scrollAmount -= boxWidth + 20; // 20px là khoảng cách giữa các box
        if (scrollAmount < 0) scrollAmount = 0;
        boxWrapper.style.transform = `translateX(-${scrollAmount}px)`;
    });
});
