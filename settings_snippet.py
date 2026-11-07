# Добавь в settings.py

# В INSTALLED_APPS должно быть:
#   "django.contrib.staticfiles",

# В TEMPLATES[0] должно быть:
#   "DIRS": [BASE_DIR / "templates"],

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # для collectstatic / деплоя
