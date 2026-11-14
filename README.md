# Система бронювання (Django + Bootstrap 5)

Повний робочий проєкт за ТЗ: кімнати, бронювання, адмін-панель, календар доступності,
реєстрація/вхід, підтвердження на email (лист друкується в консоль) і стилізований фронтенд.

Моделі: `RoomType`, `Room`, `Booking` (мінімум 3, як у ТЗ).

## Запуск на Windows (PowerShell)

Відкрий папку `booking_site` у VS Code (File -> Open Folder), потім Terminal -> New Terminal.
Переконайся, що в цій папці є `manage.py` (команда `dir`).

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations rooms bookings
python manage.py migrate
python manage.py seed
python manage.py createsuperuser
python manage.py runserver
```

Відкрий у браузері: http://127.0.0.1:8000/

Якщо `venv\Scripts\activate` блокується політикою PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
venv\Scripts\activate
```

## Що де лежить

| Сторінка | Адреса |
|---|---|
| Список кімнат + фільтр за типом | `/` |
| Форма бронювання | `/bookings/new/` |
| Календар доступності | `/bookings/availability/` |
| Мої бронювання (потрібен вхід) | `/bookings/my/` |
| Реєстрація / вхід | `/bookings/signup/`, `/accounts/login/` |
| Адмін-панель (кімнати, бронювання, підтвердження/скасування) | `/admin/` |

Фронтенд: `templates/` (Bootstrap 5.3 через CDN) і `static/css/custom.css`, `static/js/main.js`.
Налаштування статики: `config/settings.py` (`STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`).

## Здача завдання (гілка, коміт, Pull Request)

Якщо проєкт уже лежить у твоєму git-репозиторії:

```powershell
git checkout main
git pull
git checkout -b feature/frontend
git add .
git commit -m "Add Bootstrap frontend and static files setup"
git push -u origin feature/frontend
```

Якщо репозиторій ще не створено: створи порожній репозиторій на GitHub, потім

```powershell
git init
git add .
git commit -m "Initial booking project"
git branch -M main
git remote add origin <посилання_на_репозиторій>
git push -u origin main
git checkout -b feature/frontend
```

Після цього внеси свої зміни у фронтенд, зроби коміт, `git push -u origin feature/frontend`
і створи Pull Request на GitHub. Скріншоти сайту перетягни в опис PR.
