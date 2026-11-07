from django.conf import settings
from django.core.mail import send_mail


def send_booking_email(booking):
    """Надсилає лист про створення/зміну статусу бронювання.

    У розробці лист друкується в консоль (EMAIL_BACKEND у settings.py).
    """
    subject = f"Бронювання #{booking.pk}: {booking.get_status_display()}"
    message = (
        f"Вітаємо, {booking.guest_name}!\n\n"
        f"Кімната: {booking.room.name}\n"
        f"Період: {booking.start_date:%d.%m.%Y} - {booking.end_date:%d.%m.%Y} "
        f"({booking.days} дн.)\n"
        f"Вартість: {booking.total_price} грн\n"
        f"Статус: {booking.get_status_display()}\n\n"
        "Дякуємо, що користуєтесь нашою системою бронювання."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email],
        fail_silently=True,
    )
