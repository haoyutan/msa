import os


def get_msa_settings(BASE_DIR,
                     DATA_DIR,
                     DEBUG=True,
                     SECURE_COOKIE=False,
                     USE_MSA_DEFAULT_DATABASES=True,
                     STATIC_URL='/django-static/',
                     STATIC_ROOT_REL='deploy/web/django-static/'):
    settings = {}

    LOG_DIR = os.path.join(DATA_DIR, 'log')
    os.makedirs(LOG_DIR, exist_ok=True)

    DB_DIR = os.path.join(DATA_DIR, 'db')
    os.makedirs(DB_DIR, exist_ok=True)

    # Settings for rest framwork
    settings['REST_FRAMEWORK'] = {
        'DEFAULT_PERMISSION_CLASSES': ('msa_framework.permissions.DenyAny',),
        'DEFAULT_AUTHENTICATION_CLASSES': (),
    }

    # Add settings for HTTPS
    settings['SECURE_PROXY_SSL_HEADER'] = ('HTTP_X_FORWARDED_PROTO', 'https')
    settings['SESSION_COOKIE_SECURE'] = SECURE_COOKIE
    settings['CSRF_COOKIE_SECURE'] = SECURE_COOKIE

    # Add settings for logging
    settings['LOGGING'] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s.%(msecs)03d|%(levelname)s|%(name)s|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'files-django': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'django.log'),
                'maxBytes': 1073844224,
                'backupCount': 10,
                'encoding': 'UTF-8',
                'formatter': 'verbose',
            },
            'files-app': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'app.log'),
                'maxBytes': 1073844224,
                'backupCount': 10,
                'encoding': 'UTF-8',
                'formatter': 'verbose',
            },
            'files-api': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'api.log'),
                'maxBytes': 1073844224,
                'backupCount': 10,
                'encoding': 'UTF-8',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            '': {
                'handlers': ['files-app'],
                'level': 'DEBUG' if DEBUG else 'INFO',
                'propagate': True,
            },
            'API': {
                'handlers': ['files-api'],
                'level': 'INFO',
                'propagate': True,
            },
            'django': {
                'handlers': ['files-django'],
                'level': 'DEBUG' if DEBUG else 'INFO',
                'propagate': False,
            },
        },
    }

    # Update settings for static files
    settings['STATIC_URL'] = STATIC_URL
    STATIC_ROOT = os.path.join(DATA_DIR, STATIC_ROOT_REL)
    settings['STATIC_ROOT'] = STATIC_ROOT
    os.makedirs(STATIC_ROOT, exist_ok=True)

    # Update settings for databases
    if USE_MSA_DEFAULT_DATABASES:
        settings['DATABASES'] = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(DB_DIR, 'db.sqlite3'),
            }
        }

    return settings


def get_msa_settings_development(BASE_DIR):
    return get_msa_settings(BASE_DIR, DATA_DIR=BASE_DIR, DEBUG=True)


def get_msa_settings_production(BASE_DIR, DEBUG=False):
    return get_msa_settings(BASE_DIR, DATA_DIR='/data', DEBUG=DEBUG,
                            SECURE_COOKIE=True)
