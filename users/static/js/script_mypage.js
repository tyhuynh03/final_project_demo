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