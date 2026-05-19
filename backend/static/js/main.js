document.addEventListener('DOMContentLoaded', function() {
    console.log("Main JS loaded");

    // 1. Table Search / Filtering
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableId = this.dataset.target;
            const table = document.getElementById(tableId);
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const searchableCells = row.querySelectorAll('td:not(.text-end)');
                let combinedText = "";
                searchableCells.forEach(cell => {
                    const clone = cell.cloneNode(true);
                    const forms = clone.querySelectorAll('form, select, button');
                    forms.forEach(f => f.remove());
                    combinedText += clone.innerText.toLowerCase() + " ";
                });

                row.style.display = combinedText.includes(searchTerm) ? '' : 'none';
            });
        });
    });

    // 2. SweetAlert2 Confirmations
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.confirm-delete');
        if (btn) {
            e.preventDefault();
            const form = btn.closest('form');
            const message = btn.dataset.message || 'Are you sure you want to delete this?';

            Swal.fire({
                title: 'Are you sure?',
                text: message,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#dc3545',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Yes, proceed!'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        }
    });

    // 3. Flash Messages with SweetAlert2
    const flashMessages = document.querySelectorAll('.flash-data');
    flashMessages.forEach((msg, index) => {
        const category = msg.dataset.category;
        const text = msg.dataset.message;

        let icon = 'info';
        if (category === 'success') icon = 'success';
        if (category === 'danger' || category === 'error') icon = 'error';
        if (category === 'warning') icon = 'warning';

        setTimeout(() => {
            Swal.fire({
                toast: true,
                position: 'top-end',
                icon: icon,
                title: text,
                showConfirmButton: false,
                timer: 4000,
                timerProgressBar: true
            });
        }, index * 500);
    });

    // 4. Booking Page Interactivity: Show Doctor Info & Date Restrictions
    const doctorSelect = document.getElementById('doctor_id');
    if (doctorSelect) {
        const updateDoctorInfo = function() {
            const selectedOption = doctorSelect.options[doctorSelect.selectedIndex];
            if (!selectedOption || selectedOption.value === "") {
                const infoCard = document.getElementById('doctor-info-card');
                if (infoCard) infoCard.classList.add('d-none');
                return;
            }

            const bio = selectedOption.dataset.bio;
            const specialty = selectedOption.dataset.specialty;

            const infoCard = document.getElementById('doctor-info-card');
            if (infoCard && (bio || specialty)) {
                document.getElementById('info-specialty').textContent = specialty || 'General Practice';
                document.getElementById('info-bio').textContent = bio || 'No biography available.';

                if (infoCard.classList.contains('d-none')) {
                    infoCard.classList.remove('d-none');
                    infoCard.classList.add('animate__animated', 'animate__fadeIn');
                }
            } else if (infoCard) {
                infoCard.classList.add('d-none');
            }
        };
        doctorSelect.addEventListener('change', updateDoctorInfo);
        if (doctorSelect.value) updateDoctorInfo();

        // Prevent past dates in booking
        const dateInput = document.getElementById('date');
        if (dateInput) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.setAttribute('min', today);
        }
    }
});
