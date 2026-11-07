from django.contrib import admin
from django.core.exceptions import ValidationError

from .emails import send_booking_email
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guest_name",
        "email",
        "room",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "room__room_type", "room")
    search_fields = ("guest_name", "email")
    date_hierarchy = "start_date"
    actions = ["confirm_bookings", "cancel_bookings"]

    @admin.action(description="Підтвердити вибрані бронювання")
    def confirm_bookings(self, request, queryset):
        done, skipped = 0, 0
        for booking in queryset.exclude(status=Booking.Status.CONFIRMED):
            booking.status = Booking.Status.CONFIRMED
            try:
                booking.full_clean()
            except ValidationError:
                skipped += 1
                continue
            booking.save()
            send_booking_email(booking)
            done += 1
        msg = f"Підтверджено: {done}."
        if skipped:
            msg += f" Пропущено через перетин дат: {skipped}."
        self.message_user(request, msg)

    @admin.action(description="Скасувати вибрані бронювання")
    def cancel_bookings(self, request, queryset):
        done = 0
        for booking in queryset.exclude(status=Booking.Status.CANCELLED):
            booking.status = Booking.Status.CANCELLED
            booking.save()
            send_booking_email(booking)
            done += 1
        self.message_user(request, f"Скасовано: {done}.")
