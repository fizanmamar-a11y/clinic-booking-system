// Clinic Booking System JS
console.log("Clinic app loaded");

// Example: auto-dismiss alerts after 5 seconds
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.classList.remove("show");
    }, 5000);
  });
});
