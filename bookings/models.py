from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from rooms.models import Room


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Очікує підтвердження"
        CONFIRMED = "confirmed", "Підтверджено"
        CANCELLED = "cancelled", "Скасовано"

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Кімната",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        verbose_name="Користувач",
    )
    guest_name = models.CharField("Ім'я", max_length=150)
    email = models.EmailField("Електронна пошта")
    start_date = models.DateField("Дата початку")
    end_date = models.DateField("Дата завершення")
    status = models.CharField(
        "Статус", max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "бронювання"
        verbose_name_plural = "бронювання"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.room} ({self.start_date} - {self.end_date})"

    @property
    def days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_price(self):
        return self.days * self.room.price

    @property
    def badge_class(self):
        return {
            self.Status.CONFIRMED: "bg-success",
            self.Status.CANCELLED: "bg-secondary",
        }.get(self.status, "bg-warning text-dark")

    def clean(self):
        super().clean()
        if not (self.start_date and self.end_date):
            return

        if self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "Дата завершення не може бути раніше за дату початку."}
            )

        if self.room_id and self.status != self.Status.CANCELLED:
            overlapping = Booking.objects.filter(
                room_id=self.room_id,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            ).exclude(status=self.Status.CANCELLED)
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)
            if overlapping.exists():
                raise ValidationError(
                    "На обраний період ця кімната вже заброньована. "
                    "Оберіть інші дати або іншу кімнату."
                )
