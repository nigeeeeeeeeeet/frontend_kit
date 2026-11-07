document.addEventListener("DOMContentLoaded", function () {
  // Автоматично ховаємо повідомлення через 6 секунд
  document.querySelectorAll(".alert-dismissible").forEach(function (el) {
    setTimeout(function () {
      bootstrap.Alert.getOrCreateInstance(el).close();
    }, 6000);
  });

  // У формі бронювання дата завершення не може бути раніше за дату початку
  var start = document.getElementById("id_start_date");
  var end = document.getElementById("id_end_date");
  if (start && end) {
    start.addEventListener("change", function () {
      end.min = start.value;
      if (end.value && end.value < start.value) {
        end.value = start.value;
      }
    });
  }
});
