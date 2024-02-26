document.getElementById('rejectButton').addEventListener('click', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // Show SweetAlert confirmation
    Swal.fire({
        title: 'Are you sure?',
        text: 'You won\'t be able to revert this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, reject it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // If the user confirms, submit the form
            document.getElementById('rejectForm').submit();
        }
    });
});