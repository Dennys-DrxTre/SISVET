import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR / 'db.sqlite3'),
    }
}

POSTGRESQL = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB',
        'USER': 'postgres',
        'PASSWORD': 'familia58',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

MYSQL = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sisvet',
        'USER': 'root',
        'PASSWORD': 'familia58',
        'HOST': 'localhost',
        'PORT': '3306'
    }

}
