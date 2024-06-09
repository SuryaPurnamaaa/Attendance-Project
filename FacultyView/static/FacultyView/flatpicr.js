document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#datepicker", {
      enableTime: false, // Mengaktifkan pilihan tanggal saja, tanpa waktu
      dateFormat: "Y-m-d", // Format tanggal yang diinginkan
      defaultDate: "today" // Tanggal default yang ditampilkan adalah hari ini
    });
  });