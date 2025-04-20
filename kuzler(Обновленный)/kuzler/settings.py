"""
Django settings for kuzler project.
"""
# Добавьте в settings.py
DEFAULT_CHARSET = 'utf-8'
import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность (только для разработки!)
SECRET_KEY = 'django-insecure-ваш-случайный-ключ'  # Замените на уникальный!
DEBUG = True  # В продакшене ставить False!
ALLOWED_HOSTS = ['*']  # Для разработки. В продакшене указать конкретные хосты.

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # DRF
    'products',  # Ваше приложение
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'kuzler.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# База данных (SQLite по умолчанию)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей (отключена для простоты)
AUTH_PASSWORD_VALIDATORS = []

# Интернационализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медиафайлы (аудио)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DRF (без аутентификации)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Доступ без авторизации
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# Прочее
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Логирование (для отладки)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'products': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Настройки локализации
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = True

# Настройки кодировки
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'