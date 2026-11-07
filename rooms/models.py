from django.core.validators import MinValueValidator
from django.db import models


class RoomType(models.Model):
    name = models.CharField("Назва типу", max_length=100, unique=True)

    class Meta:
        verbose_name = "тип кімнати"
        verbose_name_plural = "типи кімнат"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField("Назва", max_length=150)
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name="rooms",
        verbose_name="Тип",
    )
    description = models.TextField("Опис", blank=True)
    capacity = models.PositiveIntegerField(
        "Місткість (осіб)", default=1, validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        "Ціна за добу, грн",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    features = models.CharField(
        "Особливості (через кому)",
        max_length=255,
        blank=True,
        help_text="Наприклад: Wi-Fi, Проєктор, Кондиціонер",
    )
    is_active = models.BooleanField("Доступна для бронювання", default=True)

    class Meta:
        verbose_name = "кімната"
        verbose_name_plural = "кімнати"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def features_list(self):
        return [f.strip() for f in self.features.split(",") if f.strip()]
