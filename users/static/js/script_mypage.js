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
    const totalBoxes = document.querySelectorAll(".box").length;
    let scrollAmount = 0;

    nextBtn.addEventListener("click", function () {
        if (scrollAmount < (totalBoxes - 1) * (boxWidth + 20)) { // Kiểm tra không chạm vào cuối danh sách
            scrollAmount += boxWidth + 20;
            if (scrollAmount > (totalBoxes - 1) * (boxWidth + 20)) {
                scrollAmount = (totalBoxes - 1) * (boxWidth + 20);
            }
            boxWrapper.style.transform = `translateX(-${scrollAmount}px)`;
        }
    });

    prevBtn.addEventListener("click", function () {
        if (scrollAmount > 0) { // Kiểm tra không chạm vào đầu danh sách
            scrollAmount -= boxWidth + 20;
            if (scrollAmount < 0) scrollAmount = 0;
            boxWrapper.style.transform = `translateX(-${scrollAmount}px)`;
        }
    });
}); 