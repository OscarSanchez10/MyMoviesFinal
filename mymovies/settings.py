"""
Configuración de Django para el proyecto mymovies.

Generado por 'django-admin startproject' utilizando Django 5.0.3.

Para obtener más información sobre este archivo, consulte
https://docs.djangoproject.com/en/5.0/topics/settings/

Para ver la lista completa de configuraciones y sus valores, consulte
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Construir rutas dentro del proyecto de esta manera: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuraciones de inicio rápido para desarrollo - no apto para producción
# Consulte https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantenga la clave secreta utilizada en producción en secreto!
SECRET_KEY = 'django-insecure-lu6m-a_81pzb020&5f8ds@l&6@bozq#yvl)u*!vonmi9*1rdp3'

# ADVERTENCIA DE SEGURIDAD: ¡no ejecute con depuración activada en producción!
DEBUG = True

ALLOWED_HOSTS = ['3.233.93.40']


# Definición de aplicaciones

INSTALLED_APPS = [
    'movies.apps.MoviesConfig',  # Aplicación personalizada 'movies'
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Para el formateo humano de datos
]

# Middlewares

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URL raíz

ROOT_URLCONF = 'mymovies.urls'

# Plantillas

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
                'movies.context_processors.user_context',  # Contexto personalizado de usuario
            ],
        },
    },
]

# Aplicación WSGI

WSGI_APPLICATION = 'mymovies.wsgi.application'


# Base de datos

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Motor de base de datos PostgreSQL
        "NAME": "django_bootstrap",  # Nombre de la base de datos
        "USER": "ubuntu",  # Usuario de la base de datos
        "PASSWORD": "thisissomeseucrepassword",  # Contraseña de la base de datos
        "HOST": "127.0.0.1",  # Host de la base de datos
        "PORT": "5432",  # Puerto de la base de datos
    }
}

# Validación de contraseñas

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalización

LANGUAGE_CODE = 'en-us'  # Código de idioma

TIME_ZONE = 'UTC'  # Zona horaria

USE_I18N = True  # Habilitar internacionalización

USE_TZ = True  # Usar zona horaria

# Archivos estáticos (CSS, JavaScript, imágenes)

STATIC_URL = 'static/'

# Tipo de campo de clave primaria predeterminado

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
