# See https://docs.djangoproject.com/en/2.0/topics/logging/.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['app_logs'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['app_logs'],
            'level': 'ERROR',
        },
        'requests.packages.urllib3.connectionpool': {
            'handlers': ['app_logs'],
            'level': 'ERROR',  # Quiet very verbose HTTP logging.
        },
    },

    'root': {
        'handlers': ['app_logs'],
        'level': 'DEBUG'
    },

    'formatters': {
        'detail': {
            'format': '%(asctime)s  %(levelname)s  %(pathname)s:%(lineno)d  %(funcName)s()  %(message)s',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },

        'sql': {
            'format': '%(asctime)s %(duration)s %(sql)s %(params)s',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
    },

    'handlers': {
        'app_logs': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  '/tmp/doublehelix.log',
            'formatter': 'detail',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/doublehelix_sql.log',
            'formatter': 'sql',
        },
        'null': {
            'level': 'ERROR',
            'class':'logging.NullHandler',
        },
    },
}
