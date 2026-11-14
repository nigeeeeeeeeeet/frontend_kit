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
python manage.py makemigrations accounts rooms bookings
python manage.py migrate
python manage.py seed
python manage.py createsuperuser
python manage.py runserver
```

Відкрий у браузері: http://127.0.0.1:8000/

> ⚠️ Проєкт використовує кастомну модель користувача `accounts.User`. Якщо у вас уже є
> `db.sqlite3`, створений зі стандартним `auth.User`, **видаліть його** і виконайте
> `migrate` заново: змінити `AUTH_USER_MODEL` після першої міграції Django не підтримує.

Тести: `python manage.py test accounts`.

Якщо `venv\Scripts\activate` блокується політикою PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
venv\Scripts\activate
```

## Автентифікація

- Застосунок `accounts`: кастомна модель `User(AbstractUser)` (унікальний `email`, `phone`).
- `AUTH_USER_MODEL = "accounts.User"` у `config/settings.py`.
- Власні views: `signup`, `login_view`, `logout_view` (`accounts/views.py`), форми `RegisterForm`, `LoginForm`.
- Шаблони: `templates/accounts/login.html`, `templates/accounts/signup.html` (Bootstrap).
- `@login_required`: `booking_create`, `booking_success`, `my_bookings`. Після входу
  користувач повертається на сторінку з параметра `?next=` (перевіряється на безпечність).

## Що де лежить

| Сторінка | Адреса |
|---|---|
| Список кімнат + фільтр за типом | `/` |
| Календар доступності | `/bookings/availability/` |
| Форма бронювання, мої бронювання (потрібен вхід, `@login_required`) | `/bookings/new/`, `/bookings/my/` |
| Реєстрація / вхід | `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/` (POST) |
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
