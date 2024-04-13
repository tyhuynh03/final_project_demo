document.addEventListener("DOMContentLoaded", function () {
    var showCreateUserFormButton = document.getElementById("show-create-user-form");
    var createUserForm = document.getElementById("create-user-form");

    showCreateUserFormButton.addEventListener("click", function (event) {
        event.preventDefault();
        createUserForm.style.display = "block";
    });
});
function confirmDelete(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        const form = document.getElementById('deleteForm' + userId);
        fetch(form.action, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
            }
        })
            .then(response => {
                if (response.ok) {
                    alert('User deleted successfully');
                    window.location.reload();
                    // Do any additional actions if needed
                } else {
                    throw new Error('Failed to delete user');
                }
            })
            .catch(error => {
                console.error(error);
                alert('Failed to delete user');
            });
    }
}
function logout() {
    var form = document.getElementById('logout-form');
    form.submit();
}