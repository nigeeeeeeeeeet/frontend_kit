// Автоматично ховаємо alert-повідомлення через 5 секунд
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".alert-dismissible").forEach(function (el) {
    setTimeout(function () {
      var alert = bootstrap.Alert.getOrCreateInstance(el);
      alert.close();
    }, 5000);
  });
});
