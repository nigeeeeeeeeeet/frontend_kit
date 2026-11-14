from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомна модель користувача.

    Розширює стандартного AbstractUser: email обов'язковий та унікальний,
    додано необов'язковий телефон. Вхід виконується за логіном (username).
    """

    email = models.EmailField("Електронна пошта", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)

    class Meta:
        verbose_name = "користувач"
        verbose_name_plural = "користувачі"

    def __str__(self):
        return self.username
