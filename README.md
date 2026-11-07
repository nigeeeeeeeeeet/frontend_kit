# Фронтенд для системы бронирования (Django + Bootstrap 5)

## 1. Ветка

```bash
git checkout main
git pull
git checkout -b feature/frontend
```

## 2. Статика в Django

Скопируй содержимое `settings_snippet.py` в свой `settings.py`.
Проверь:

- в `INSTALLED_APPS` есть `django.contrib.staticfiles`
- в `TEMPLATES[0]["DIRS"]` есть `BASE_DIR / "templates"`

## 3. Файлы

Скопируй в корень проекта (рядом с `manage.py`):

```
static/css/custom.css
static/js/main.js
templates/base.html
templates/rooms/room_list.html      (пример)
templates/bookings/booking_form.html (пример)
```

В примерах подставь свои имена: `rooms`, `room.name`, `room.price`, `room.capacity`, url-имена (`booking_create` и т.д.).

## 4. Подключение шаблонов

Каждый шаблон должен начинаться с:

```django
{% extends "base.html" %}
{% block content %}
...
{% endblock %}
```

## 5. Коммиты

```bash
git add settings.py templates/base.html static/
git commit -m "Add static files config and Bootstrap base template"

git add templates/
git commit -m "Style room list and booking form with Bootstrap"

git add static/css/custom.css
git commit -m "Add custom CSS"
```

## 6. Проверка

```bash
python manage.py runserver
```

Если стили не подтянулись: DevTools -> Network, смотри 404 на `/static/...`.

## 7. Pull Request

```bash
git push -u origin feature/frontend
```

На GitHub: Compare & pull request, `feature/frontend` -> `main`.
В описание перетащи скриншоты сайта. Ссылку на PR отправь преподавателю.
