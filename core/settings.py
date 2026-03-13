import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$p$07d-_)&8e1n1*8jt%@=#7%nintd298ocwda9gb8$%==dpsx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Railway ላይ እንዲሰራ '*' የግድ ያስፈልጋል
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export', 
    'crm_app',
    'crm_app',
    'inventory',  # ይህ ሲጨመር ነው በጎን በኩል 'Inventory' የሚለው የሚመጣው
    'import_export', # ይህ መኖሩን አረጋግጥ
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# PythonAnywhere አድራሻን ወደ BASE_DIR ቀይረነዋል
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/app/data/db.sqlite3', # አዲሱ አድራሻ ይሄ ነው
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'uniqueuna7@gmail.com'
EMAIL_HOST_PASSWORD = 'ijkbddehwzupgtqx'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Import Export Settings (Safe Version)
try:
    import import_export.formats.base_formats
    IMPORT_EXPORT_FORMATS = [
        import_export.formats.base_formats.CSV,
        import_export.formats.base_formats.XLSX
    ]
except ImportError:
    pass
CSRF_TRUSTED_ORIGINS = [
    'https://mgk-hosecrm-production.up.railway.app',
]
SESSION_COOKIE_AGE = 300
SESSION_SAVE_EVERY_REQUEST = True
IMPORT_EXPORT_TMP_STORAGE_CLASS = 'import_export.tmp_storages.TempFolderStorage'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000
