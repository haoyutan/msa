import os


MSA_CONFIG_DEFAULT = {
    'DEBUG'               : True,
    'MSA_DATA_DIR'        : None,
    'STATIC_URL'          : '/django-static/',
    'MSA_STATIC_ROOT'     : 'django-static/',
    'MSA_HTTPS'           : False,
    'MSA_DEFAULT_DB'      : True,
    'MSA_LOGGING'         : True,
    'MSA_ALLOW_ADMIN_SITE': False,
}

MSA_CONFIG_DEVELOPMENT_DEFAULT = MSA_CONFIG_DEFAULT.copy()
MSA_CONFIG_DEVELOPMENT_DEFAULT.update({
    'MSA_ALLOW_ADMIN_SITE': True,
})

MSA_CONFIG_PRODUCTION_DEFAULT = MSA_CONFIG_DEFAULT.copy()
MSA_CONFIG_PRODUCTION_DEFAULT.update({
    'DEBUG'               : False,
    'MSA_HTTPS'           : True,
    'MSA_ALLOW_ADMIN_SITE': True,
})

MSA_CONFIG_DOCKER_DEFAULT = MSA_CONFIG_DEFAULT.copy()
MSA_CONFIG_DOCKER_DEFAULT.update({
    'DEBUG'               : False,
    'MSA_HTTPS'           : True,
    'MSA_ALLOW_ADMIN_SITE': True,
    'MSA_DATA_DIR'        : '/data',
    'MSA_STATIC_ROOT'     : 'deploy/web/django-static/',
})


class MSASettings:

    def __init__(self, django_settings, msa_config=MSA_CONFIG_DEFAULT):
        self._msa_config = msa_config
        self._django_settings = django_settings
        self._settings = django_settings.copy()
        self._update_settings()

    @property
    def msa_config(self):
        return self._msa_config

    @property
    def settings(self):
        return self._settings

    def update_django_settings(self, django_settings=None):
        if not django_settings:
            django_settings = self._django_settings
        django_settings.update(self.settings)

    def _update_settings(self):
        self._update_msa_data_dir()
        self._update_debug()
        self._update_static()
        self._update_https()
        self._update_db()
        self._update_logging()
        self._update_rest_framework()
        self._update_allow_admin_site()

    def _update_msa_data_dir(self):
        msa_data_dir = self.msa_config.get('MSA_DATA_DIR', None)
        if msa_data_dir:
            self.settings['MSA_DATA_DIR'] = msa_data_dir
        else:
            self.settings['MSA_DATA_DIR'] = self.settings.get('BASE_DIR')

    def _update_debug(self):
        debug = self.msa_config.get('DEBUG', False)
        self.settings['DEBUG'] = debug

        '''
        If DEBUG is False, ALLOWED_HOSTS must be set properly. Otherwise,
        Nginx will return BAD REQUEST (400) error. For convenience, we
        automatically set ALLOWED_HOSTS to ["*",] if it is empty and
        DEBUG is False. However, we will not change ALLOWED_HOSTS if it is
        not empty (which implies that it is already set).
        '''
        if not debug and len(self.settings['ALLOWED_HOSTS']) == 0:
            self.settings['ALLOWED_HOSTS'] = ['*',]

    def _update_static(self):
        self.settings['STATIC_URL'] = self.msa_config.get('STATIC_URL')

        msa_data_dir = self.settings['MSA_DATA_DIR']
        msa_static_root_rel = self.msa_config.get('MSA_STATIC_ROOT')
        static_root = os.path.join(msa_data_dir, msa_static_root_rel)
        self.settings['STATIC_ROOT'] = static_root
        os.makedirs(static_root, exist_ok=True)

    def _update_https(self):
        msa_https = self.msa_config.get('MSA_HTTPS', False)
        if msa_https:
            self.settings['SECURE_PROXY_SSL_HEADER'] = (
                'HTTP_X_FORWARDED_PROTO', 'https'
            )
            self.settings['SESSION_COOKIE_SECURE'] = True
            self.settings['CSRF_COOKIE_SECURE'] = True

    def _update_db(self):
        msa_default_db = self.msa_config.get('MSA_DEFAULT_DB', False)
        if not msa_default_db:
            return

        db_dir = os.path.join(self.settings['MSA_DATA_DIR'], 'db')
        os.makedirs(db_dir, exist_ok=True)
        self.settings['DATABASES'].update({
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(db_dir, 'db.sqlite3'),
            }
        })

    def _update_logging(self):
        msa_logging = self.msa_config.get('MSA_LOGGING', True)
        if not msa_logging:
            return

        debug = self.settings['DEBUG']
        log_dir = os.path.join(self.settings['MSA_DATA_DIR'], 'log')
        os.makedirs(log_dir, exist_ok=True)
        self.settings['LOGGING'] = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(asctime)s.%(msecs)03d|%(levelname)s|'
                              '%(name)s|%(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                },
            },
            'handlers': {
                'files-django': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(log_dir, 'django.log'),
                    'maxBytes': 1073844224,
                    'backupCount': 10,
                    'encoding': 'UTF-8',
                    'formatter': 'verbose',
                },
                'files-app': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(log_dir, 'app.log'),
                    'maxBytes': 1073844224,
                    'backupCount': 10,
                    'encoding': 'UTF-8',
                    'formatter': 'verbose',
                },
                'files-api': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(log_dir, 'api.log'),
                    'maxBytes': 1073844224,
                    'backupCount': 10,
                    'encoding': 'UTF-8',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['files-app'],
                    'level': 'DEBUG' if debug else 'INFO',
                    'propagate': False,
                },
                'API': {
                    'handlers': ['files-api'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'django': {
                    'handlers': ['files-django'],
                    'level': 'DEBUG' if debug else 'INFO',
                    'propagate': False,
                },
            },
        }

    def _update_rest_framework(self):
        self.settings['REST_FRAMEWORK'] = {
            'DEFAULT_PERMISSION_CLASSES': ('msa.permissions.DenyAny',),
            'DEFAULT_AUTHENTICATION_CLASSES': (),
        }

    def _update_allow_admin_site(self):
        self.settings['MSA_ALLOW_ADMIN_SITE'] = \
            self.msa_config.get('MSA_ALLOW_ADMIN_SITE', False)


def update_django_settings(django_settings, user_msa_config={}):
    env = os.environ.get('MSA_DEPLOYMENT_ENV', 'development')
    if env == 'development':
        msa_config = MSA_CONFIG_DEVELOPMENT_DEFAULT.copy()
    elif env == 'production':
        msa_config = MSA_CONFIG_PRODUCTION_DEFAULT.copy()
    elif env == 'docker':
        msa_config = MSA_CONFIG_DOCKER_DEFAULT.copy()
    else:
        raise ValueError('The value of environment variable '
                         'MSA_DEPLOYMENT_ENV should be \'development\', '
                         '\'production\', or \'docker\'.')

    if user_msa_config:
        msa_config.update(user_msa_config)

    MSASettings(django_settings, msa_config).update_django_settings()
