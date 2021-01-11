from config import LoggerConfig

LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'simple': { 
            'format': '%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s'
        },
        'complex':{
            'format': '%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s   call_trace=%(pathname)s L%(lineno)-4d'
        }
    },
    'handlers': { 
        'screen': { 
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': f'{LoggerConfig.dir_path}/out.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
        }
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['file', 'screen'],
            'level': 'DEBUG',
        },
    } 
}