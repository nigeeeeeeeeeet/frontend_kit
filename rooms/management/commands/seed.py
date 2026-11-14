from datetime import date, timedelta

from django.core.management.base import BaseCommand

from bookings.models import Booking
from rooms.models import Room, RoomType


class Command(BaseCommand):
    help = "Додає тестові типи кімнат, кімнати та кілька бронювань"

    def handle(self, *args, **options):
        type_names = ["Конференц-зал", "Переговорна", "Коворкінг", "Банкетний зал"]
        types = {n: RoomType.objects.get_or_create(name=n)[0] for n in type_names}

        rooms_data = [
            ("Зал «Київ»", "Конференц-зал", 120, 8000,
             "Wi-Fi, Проєктор, Сцена, Звук",
             "Простора зала для конференцій та презентацій."),
            ("Зал «Львів»", "Конференц-зал", 60, 4500,
             "Wi-Fi, Проєктор, Кондиціонер",
             "Затишна зала для семінарів і тренінгів."),
            ("Переговорна «Альфа»", "Переговорна", 8, 1200,
             "Wi-Fi, Екран, Маркерна дошка",
             "Невелика кімната для зустрічей команди."),
            ("Переговорна «Бета»", "Переговорна", 12, 1800,
             "Wi-Fi, Відеозв'язок, Кондиціонер",
             "Кімната для переговорів із клієнтами."),
            ("Коворкінг «Open Space»", "Коворкінг", 25, 2500,
             "Wi-Fi, Кава, Принтер",
             "Відкритий простір із робочими місцями."),
            ("Банкетний зал «Золотий»", "Банкетний зал", 80, 12000,
             "Кухня, Сцена, Парковка, Звук",
             "Зал для весіль, ювілеїв та корпоративів."),
        ]

        for name, type_name, capacity, price, features, description in rooms_data:
            Room.objects.get_or_create(
                name=name,
                defaults={
                    "room_type": types[type_name],
                    "capacity": capacity,
                    "price": price,
                    "features": features,
                    "description": description,
                },
            )

        if not Booking.objects.exists():
            today = date.today()
            rooms = list(Room.objects.all())
            samples = [
                (rooms[0], 2, 4, "confirmed", "Олена Коваленко", "olena@example.com"),
                (rooms[2], 1, 1, "pending", "Андрій Мельник", "andrii@example.com"),
                (rooms[3], 5, 7, "confirmed", "Ірина Шевченко", "iryna@example.com"),
                (rooms[4], 3, 9, "pending", "Максим Бондар", "maksym@example.com"),
                (rooms[5], 10, 11, "confirmed", "Софія Ткаченко", "sofia@example.com"),
            ]
            for room, offset, length, status, name, email in samples:
                start = today + timedelta(days=offset)
                Booking.objects.create(
                    room=room,
                    guest_name=name,
                    email=email,
                    start_date=start,
                    end_date=start + timedelta(days=length - 1),
                    status=status,
                )

        self.stdout.write(self.style.SUCCESS("Тестові дані додано."))
